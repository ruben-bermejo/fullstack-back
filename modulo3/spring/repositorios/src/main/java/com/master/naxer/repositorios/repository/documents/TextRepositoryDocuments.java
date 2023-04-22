package com.master.naxer.repositorios.repository.documents;

import com.master.naxer.repositorios.entity.documents.TextT;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TextRepositoryDocuments extends MongoRepository<TextT, Integer> {
}
