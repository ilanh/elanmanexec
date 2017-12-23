FROM ubuntu:16.04

# Set terminal to be noninteractive
ENV DEBIAN_FRONTEND noninteractive
ENV ANSIBLE_ROLES_PATH /code

# Install packages
RUN apt-get update && apt-get install -y \
    git \
    software-properties-common \
    openssh-server \
    nginx \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    supervisor \
    vim
RUN pip3 install --upgrade pip && \
    apt-add-repository ppa:ansible/ansible -y && \
    apt-get update && \
    apt-get install -y ansible

# Configure Django project
ADD . /code
RUN mkdir /files /files/static /files/media /logs /logs/nginx /logs/gunicorn
WORKDIR /code
RUN pip3 install -r requirements.txt
RUN chmod ug+x /code/initialize.sh

# Generate key for root and copy it ro authorized keys
RUN ssh-keygen -t rsa -f "/root/.ssh/id_rsa" -N "" -q && cp /root/.ssh/id_rsa.pub \
    /root/.ssh/authorized_keys && cp /code/sshconfig /root/.ssh/config
# Get elanman
# Production use galaxy
RUN ansible-galaxy install ilanh.elanman
WORKDIR ilanh.elanman
# Develop use github
# RUN git clone -b develop https://github.com/ilanh/elanman.git .
# Production has yml extentions remove when merge develop
RUN service ssh start && ansible-playbook -i managers.sample elanman.yml -e "destinationDir=/code/myelanman"
# Develop use new yaml extention
# RUN service ssh start && ansible-playbook -i managers.sample elanman.yaml -e "destinationDir=/code/myelanman, staticDir=/files/portal"

# Expose ports
# 22 = ssh
# 80 = Nginx
# 8000 = Gunicorn
EXPOSE 22 80 8000

# Configure Nginx
RUN ln -s /code/nginx.conf /etc/nginx/sites-enabled/portal.conf
RUN rm /etc/nginx/sites-enabled/default

# Run Supervisor (i.e., start MySQL, Nginx, and Gunicorn)
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]
