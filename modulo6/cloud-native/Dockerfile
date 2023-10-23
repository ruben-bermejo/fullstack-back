FROM docker.io/tomcat:10.1
RUN rm -rf /usr/local/tomcat/webapps
RUN mv /usr/local/tomcat/webapps.dist /usr/local/tomcat/webapps
COPY repositorios-app.war /usr/local/tomcat/webapps/repositorios-app.war
COPY tomcat-users.xml /usr/local/tomcat/conf/tomcat-users.xml
COPY context.xml /usr/local/tomcat/webapps/manager/META-INF/context.xml
EXPOSE 8080
ENTRYPOINT ["catalina.sh", "run"]