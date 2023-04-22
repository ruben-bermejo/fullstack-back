package com.master.naxer.repositorios.repository.documents;

import com.master.naxer.repositorios.entity.documents.TextPropertiesT;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TextPropertiesRepositoryDocuments extends MongoRepository<TextPropertiesT, Integer> {
}
