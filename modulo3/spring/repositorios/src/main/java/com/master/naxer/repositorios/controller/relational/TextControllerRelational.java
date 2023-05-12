package com.master.naxer.repositorios.controller.relational;

import com.master.naxer.repositorios.entity.relational.TextT;
import com.master.naxer.repositorios.service.relational.TextServiceRelational;
import io.micrometer.core.instrument.Counter;
import io.micrometer.prometheus.PrometheusMeterRegistry;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Optional;

@RestController
@RequestMapping(path = "/relational")
public class TextControllerRelational {

    private final TextServiceRelational textServiceRelational;
    private final Counter counter;

    public TextControllerRelational(TextServiceRelational textServiceRelational, PrometheusMeterRegistry registry) {
        this.textServiceRelational = textServiceRelational;
        this.counter = Counter
                .builder("counter.print.text.relational")
                .description("indica cuántas veces es invocado el path del api")
                .register(registry);
    }

    @GetMapping(value = "/printString/{id}")
    public String printString(@PathVariable Integer id) {
        this.counter.increment();
        return this.textServiceRelational.getString(id);
    }

    @GetMapping(value = "/getText/{id}")
    public Optional<TextT> getText(@PathVariable Integer id) {
        return this.textServiceRelational.getText(id);
    }

}
