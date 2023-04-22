package com.master.naxer.repositorios.controller.relational;

import com.master.naxer.repositorios.entity.TextT;
import com.master.naxer.repositorios.service.relational.TextServiceRelational;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
@RequestMapping(path = "/relational")
public class TextControllerRelational {

    private final TextServiceRelational textServiceRelational;

    public TextControllerRelational(TextServiceRelational textServiceRelational) {
        this.textServiceRelational = textServiceRelational;
    }

    @GetMapping(value = "/printString/{id}")
    public String printString(@PathVariable Integer id) {
        return this.textServiceRelational.getString(id);
    }

    @GetMapping(value = "/getText/{id}")
    public Optional<TextT> getText(@PathVariable Integer id) {
        return this.textServiceRelational.getText(id);
    }

}
