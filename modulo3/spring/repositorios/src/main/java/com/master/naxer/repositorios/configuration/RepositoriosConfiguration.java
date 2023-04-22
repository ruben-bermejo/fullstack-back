package com.master.naxer.repositorios.configuration;

import com.master.naxer.repositorios.entity.documents.TextPropertiesT;
import com.master.naxer.repositorios.entity.documents.TextT;
import com.master.naxer.repositorios.repository.documents.TextPropertiesRepositoryDocuments;
import com.master.naxer.repositorios.repository.documents.TextRepositoryDocuments;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import javax.sql.DataSource;
import java.util.ArrayList;
import java.util.List;

@Configuration
public class RepositoriosConfiguration {

    private final String driverClass;
    private final String url;
    private final String username;
    private final String password;

    public RepositoriosConfiguration(@Value("${spring.datasource.driver-class-name}") String driverClass,
                                     @Value("${spring.datasource.url}") String url,
                                     @Value("${spring.datasource.username}") String username,
                                     @Value("${spring.datasource.password}") String password) {
        this.driverClass = driverClass;
        this.url = url;
        this.username = username;
        this.password = password;
    }

    @Bean
    public DataSource getDataSource(){
        final DataSourceBuilder<?> dataSourceBuilder = DataSourceBuilder.create();
        dataSourceBuilder.driverClassName(this.driverClass);
        dataSourceBuilder.url(this.url);
        dataSourceBuilder.username(this.username);
        dataSourceBuilder.password(this.password);
        return dataSourceBuilder.build();
    }

    @Bean
    CommandLineRunner commandLineRunnerText(final TextRepositoryDocuments textRepositoryDocuments){
        final List<TextPropertiesT> textPropertiesTList = new ArrayList<>();
        textPropertiesTList.add(new TextPropertiesT(1, null, "", null));
        textPropertiesTList.add(new TextPropertiesT(2, null, "", null));
        return strings -> {
            textRepositoryDocuments.save(new TextT(1, "Text 1 mongo", "Front", 1, textPropertiesTList));
            textRepositoryDocuments.save(new TextT(2, "Text 2 mongo", "Front", 2, textPropertiesTList));
        };
    }

    @Bean
    CommandLineRunner commandLineRunnerTextProperties(final TextPropertiesRepositoryDocuments textPropertiesRepositoryDocuments){
        return strings -> {
            textPropertiesRepositoryDocuments.save(new TextPropertiesT(1, 30, "style=\"color:blue;\"", 1));
            textPropertiesRepositoryDocuments.save(new TextPropertiesT(2, 30, "style=\"color:red;\"", 2));
        };
    }

}
