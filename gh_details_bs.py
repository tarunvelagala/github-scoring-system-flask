from bs4 import BeautifulSoup
import requests
choice="Y"
while (choice == "Y" or choice == "y"):
    gh_score=0
    url=input("Enter the url : ")
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    if(soup.title.string != 'Page not found · GitHub'):
        gh_score += 10
        print("User has a GitHub account")
        print("GitHub Score = ",gh_score)

    else:
        print("No such GitHub account found")
        break

    url_repo=url+"?tab=repositories"
    response_repo = requests.get(url_repo)
    soup_repo = BeautifulSoup(response_repo.content, 'html.parser')
    print("Forked Projects : ",end="")
    forked_commits = 0
    for sentence in soup_repo.find_all('li', {"class": "col-12 d-flex width-full py-4 border-bottom public fork"}):
        url_commits = url+"/"+sentence.h3.get_text().strip()
        response_commits = requests.get(url_commits)
        soup_commits = BeautifulSoup(response_commits.content, 'html.parser')
        c = soup_commits.find('span', {"class": "num text-emphasized"})
        #print(url_commits)
        cc = c.get_text().strip()
        cc = cc.replace(",","")
        forked_commits += int(cc) 
        if (forked_commits > 5):
            gh_score += 20
            break
    #print(forked_commits)
    print("GitHub Score = ",gh_score)

    print("Original Projects : ",end="")
    original_commits = 0
    for sentence in soup_repo.find_all('li', {"class": "col-12 d-flex width-full py-4 border-bottom public source"}):
        url_commits = url+"/"+sentence.h3.get_text().strip()
        response_commits = requests.get(url_commits)
        soup_commits = BeautifulSoup(response_commits.content, 'html.parser')
        c = soup_commits.find('span', {"class": "num text-emphasized"})
        #print(url_commits)
        cc = c.get_text().strip()
        cc = cc.replace(",","")
        original_commits += int(cc) 
        if (original_commits > 10):
            gh_score += 20
            break
    #print(original_commits)
    print("GitHub Score = ",gh_score)

    print("Final GitHub Score = ",gh_score)
    choice=input("Do you want to enter another user (Y/N) : ")
