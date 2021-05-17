#!/usr/bin/env python

import argparse
import sys
import requests
import os
import re


def run_query(query_name, header_auth, q_vars):
    with open('queries/' + query_name, 'r') as file:
        query = file.read().replace('\n', '')

    request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': q_vars }, headers=header_auth)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


def get_repos(org, header_auth):
    """
    :param org: GitHub organisation name
    :param header_auth: {"Authorization": "Bearer " + github_token} #GitHub Personal Access Token
    :return: list of repositories available for this organisation
    GitHub has rate limits up to 100 nodes for each requests
    https://docs.github.com/en/free-pro-team@latest/graphql/overview/resource-limitations#node-limit
    If number of repos over 100 we must use pagination https://graphql.org/learn/pagination/
    """
    q_vars = {"q": org}
    result = run_query('get_repos_first.graphql', header_auth, q_vars)
    repos = []
    for repo in result["data"]["organization"]["repositories"]["edges"]:
        repos.append(repo["node"]["name"])
    while bool(result["data"]["organization"]["repositories"]["pageInfo"]["hasNextPage"]):
        cursor = result["data"]["organization"]["repositories"]["pageInfo"]["endCursor"]
        q_vars = {"q": org, "cursor": cursor}
        result = run_query('get_repos_next.graphql', header_auth, q_vars)
        for repo in result["data"]["organization"]["repositories"]["edges"]:
            repos.append(repo["node"]["name"])
    return repos


def get_branches(org, header_auth, repo):
    q_vars = {"owner": org, "repo": repo}
    result = run_query('get_branches_first.graphql', header_auth, q_vars)
    branches = []
    for branch in result["data"]["repository"]["refs"]["edges"]:
        branches.append(branch["node"]["name"])
    while bool(result["data"]["repository"]["refs"]["pageInfo"]["hasNextPage"]):
        cursor = result["data"]["repository"]["refs"]["pageInfo"]["endCursor"]
        q_vars = {"owner": org, "repo": repo, "cursor": cursor}
        result = run_query('get_branches_next.graphql', header_auth, q_vars)
        for branch in result["data"]["repository"]["refs"]["edges"]:
            branches.append(branch["node"]["name"])
    return branches


def get_files(org, header_auth, repo, branch):
    q_vars = {"owner": org, "repo": repo, "expression": branch + ":"}
    result = run_query('get_files_first.graphql', header_auth, q_vars)
    files = []
    if result["data"]["repository"]["filename"]:
        for file in result["data"]["repository"]["filename"]["entries"]:
            files.append({"path": file["path"]})
    return files


def parse_files(files, name):
    matches = []
    for file in files:
        # print ("filename: ", file["path"])
        if name in file["path"]:
            matches.append(file["path"])
    return matches

def rest_api_check(org, header_auth, repo):
    URL = 'https://api.github.com/repos/' + org + '/' + repo + '/license'
    response = requests.head(URL, headers = header_auth)
    if str(response) == '<Response [200]>':
        return True




def main():
    parser = argparse.ArgumentParser(description='Github search by all branches')
    parser.add_argument('--org',
                        dest='org',
                        default="clearmatics",
                        type=str,
                        help='GitHub organisation (default: %(default)s)'
                        )
    parser.add_argument('--name',
                        dest='name',
                        default="LICENSE",
                        type=str,
                        help='Search pattern (default: %(default)s)'
                        )
    args = parser.parse_args()


    try:
        github_token = os.environ["GITHUB_PAT"]
    except KeyError:
        print("Error. GitHub PAT must be provided via environment variable")
        print("export GITHUB_PAT=")
        sys.exit(1)

    header_auth = {"Authorization": "Bearer " + github_token}
    repos_no_licence = []
    repos_wrong_branch = []

    repos = get_repos(args.org, header_auth)
    for repo in repos:
        Licence = False

        # First use REST API for an initial fast licence check on Master / Main

        Licence = rest_api_check(args.org, header_auth, repo)
        
        # Then the 'develop' branch:

        if not Licence:
            files = get_files(args.org, header_auth, repo, "develop")
            if files:
                matches = parse_files(files, args.name)
                if matches:
                    # print(f'git@github.com:{args.org}/{repo}.git -b {"develop"} \nFiles: {matches}')
                    repos_wrong_branch.append( [repo, "develop"])
                    Licence = True
        
        # Then all the others:

        if not Licence:
            branches = get_branches(args.org, header_auth, repo)
            for branch in branches:
                if not Licence:
                    files = get_files(args.org, header_auth, repo, branch)
                    if files:
                        matches = parse_files(files, args.name)
                        if matches:
                            # print(f'git@github.com:{args.org}/{repo}.git -b {branch} \nFiles: {matches}')
                            repos_wrong_branch.append( [repo, branch])

                            Licence = True

        if not Licence:
            repos_no_licence.append(repo)
    
    print ('Repos without licences: ')
    print (repos_no_licence)

    print ('Repos with licence in the wrong branch:')
    print (repos_wrong_branch)


if __name__ == '__main__':
    main()
