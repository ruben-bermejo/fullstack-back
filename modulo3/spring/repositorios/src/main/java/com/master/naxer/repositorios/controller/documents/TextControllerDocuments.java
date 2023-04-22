package com.master.naxer.repositorios.controller.documents;

import com.master.naxer.repositorios.entity.documents.TextT;
import com.master.naxer.repositorios.service.documents.TextServiceDocuments;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
@RequestMapping(path = "/documents")
public class TextControllerDocuments {

    private final TextServiceDocuments textServiceDocuments;

    public TextControllerDocuments(TextServiceDocuments textServiceDocuments) {
        this.textServiceDocuments = textServiceDocuments;
    }

    @GetMapping(value = "/printString/{id}")
    public String printString(@PathVariable Integer id) {
        return this.textServiceDocuments.getString(id);
    }

    @GetMapping(value = "/getText/{id}")
    public Optional<TextT> getText(@PathVariable Integer id) {
        return this.textServiceDocuments.getText(id);
    }

}
