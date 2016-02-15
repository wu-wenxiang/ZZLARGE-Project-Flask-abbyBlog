# Automation of deployment using fabric

Usage

    cp .fabricrc fabricrc
    modify fabricrc
    fab -c fabricrc task_name

Initial deployment

    fab -c fabricrc init_deploy_u1404

Deployment after code changes

    fab -c fabricrc deploy

Windows deploy

    Download & install VCForPython27.msi from https://www.microsoft.com/en-us/download/details.aspx?id=44266
    env\Scripts\activate
    env\Scripts\fab -c fabricrc init_deploy_u1404
    env\Scripts\fab -c fabricrc deploy

Configurations

    # change configuration in fabricrc (not .fabricrc)
