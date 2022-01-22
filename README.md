# TODO
# Git commands:
- To clone: 
    git clone https://git.ece.iastate.edu/sd/sdmay21-23.git
- To pull: 
    git checkout master
    git pull
- To check staging status:
    git status
- To commit and push: 
    git  add [relative file location and name]  (To add all changes to staging area)
    git commit -m "message" (To make a commit of all files in staging area) 
    git push    (To push all changes to the current woking branch)

# Docker commands:
- To build docker image:
    sudo docker-compose build
- To start docker containers:
    sudo docker-compose up -d
- To shut down docker image:
    sudo docker-compose down -v
- To delete unused docker images:
    sudo docker system prune