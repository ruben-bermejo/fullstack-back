package com.master.naxer.repositorios.service.relational;

import com.master.naxer.repositorios.entity.TextT;
import com.master.naxer.repositorios.repository.relational.TextRepositoryRelational;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class TextServiceRelational {

    private final TextRepositoryRelational repositoryRelational;

    public TextServiceRelational(TextRepositoryRelational repositoryRelational) {
        this.repositoryRelational = repositoryRelational;
    }

    public Optional<TextT> getText(final Integer id){
        return this.repositoryRelational.findById(id);
    }
    public String getString(final Integer id){
        Optional<TextT> texto = this.getText(id);
        return texto.isPresent() ? texto.get().getTextValue() : "Texto no encontrado!";
    }
}
