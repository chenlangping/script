# first install maven
wget https://www-us.apache.org/dist/maven/maven-3/3.6.2/binaries/apache-maven-3.6.2-bin.tar.gz

# decompress
tar -xvf apache-maven-3.6.2-bin.tar.gz
sudo mv -f apache-maven-3.6.2 /usr/local/

# install and set env
export MAVEN_HOME=/usr/local/apache-maven-3.3.9
export PATH=${PATH}:${MAVEN_HOME}/bin
mvn -v

# make a project and create some directories like this:
your project
├── pom.xml
├── project.iml(optional)
└── src
    ├── main
    │   ├── java
    │   └── resources
    └── test
        └── java

# mvn Life cycle
mvn validate

# now you can edit your code and compile
mvn compile

# use some test tools to test your project e.g. JUnit
mvn test

# create jar based on your project
mvn package

# put the jar file to your local repo to let other project to use
mvn install

