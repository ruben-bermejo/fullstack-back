package com.master.naxer.repositorios.service.documents;

import com.master.naxer.repositorios.entity.documents.TextT;
import com.master.naxer.repositorios.repository.documents.TextRepositoryDocuments;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class TextServiceDocuments {

    private final TextRepositoryDocuments repositoryDocuments;

    public TextServiceDocuments(TextRepositoryDocuments repositoryDocuments) {
        this.repositoryDocuments = repositoryDocuments;
    }

    public Optional<TextT> getText(final Integer id){
        return this.repositoryDocuments.findById(id);
    }
    public String getString(final Integer id){
        Optional<TextT> texto = this.getText(id);
        return texto.isPresent() ? texto.get().getTextValue() : "Texto no encontrado!";
    }
}
