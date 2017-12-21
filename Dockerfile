FROM ubuntu:16.04

# Enable production settings by default; for development, this can be set to 
# `false` in `docker run --env`
#ENV DJANGO_PRODUCTION=false

# Set terminal to be noninteractive
ENV DEBIAN_FRONTEND noninteractive

ENV ANSIBLE_ROLES_PATH /code

# Enable MySQL root user creation without interactive input
RUN echo 'mysql-server mysql-server/root_password password devrootpass' | debconf-set-selections
RUN echo 'mysql-server mysql-server/root_password_again password devrootpass' | debconf-set-selections

# Install packages
RUN apt-get update && apt-get install -y \
    git \
    software-properties-common \
#    libmysqlclient-dev \
#    mysql-server \
    openssh-server \
    nginx \
    python3 \
    python3-dev \
#    python3-mysqldb \
    python3-setuptools \
    python3-pip \
    supervisor \
    vim
RUN pip3 install --upgrade pip && \
    apt-add-repository ppa:ansible/ansible -y && \
    apt-get update && apt-get install -y ansible

#RUN easy_install3 pip

# Handle urllib3 InsecurePlatformWarning
#RUN apt-get install -y libffi-dev libssl-dev libpython2.7-dev
#RUN pip install urllib3[security] requests[security] ndg-httpsclient pyasn1

# Configure Django project
ADD . /code
RUN mkdir /djangomedia
RUN mkdir /static
RUN mkdir /logs
RUN mkdir /logs/nginx
RUN mkdir /logs/gunicorn
WORKDIR /code
RUN pip3 install -r requirements.txt
RUN chmod ug+x /code/initialize.sh

# Coonfigure ansible env
RUN ssh-keygen -t rsa -f "/root/.ssh/id_rsa" -N "" -q && cp /root/.ssh/id_rsa.pub \
    /root/.ssh/authorized_keys && cp /code/sshconfig /root/.ssh/config
RUN ansible-galaxy install ilanh.elanman
WORKDIR ilanh.elanman
RUN service ssh start && ansible-playbook -i managers.sample elanman.yml -e "destinationDir=/code/myelanman"

# Expose ports
# 22 = ssh
# 80 = Nginx
# 8000 = Gunicorn
# 3306 = MySQL
EXPOSE 22 80 8000
# 3306

# Configure Nginx
RUN ln -s /code/nginx.conf /etc/nginx/sites-enabled/portal.conf
RUN rm /etc/nginx/sites-enabled/default

# Run Supervisor (i.e., start MySQL, Nginx, and Gunicorn)
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
CMD ["/usr/bin/supervisord"]