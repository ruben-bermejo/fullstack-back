package com.master.naxer.repositorios.service.relational;

import com.master.naxer.repositorios.entity.relational.TextT;
import com.master.naxer.repositorios.repository.relational.TextRepositoryRelational;
import io.micrometer.core.instrument.Gauge;
import io.micrometer.prometheus.PrometheusMeterRegistry;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

@Service
public class TextServiceRelational {

    private final TextRepositoryRelational repositoryRelational;
    private final Gauge gauge;
    private final List<String> repositoryCalls = new ArrayList<>();

    public TextServiceRelational(TextRepositoryRelational repositoryRelational, PrometheusMeterRegistry registry) {
        this.repositoryRelational = repositoryRelational;
        this.gauge = Gauge
                .builder("gauge.service.relational", this.repositoryCalls, List::size)
                .register(registry);
    }

    public String getString(final Integer id){
        Optional<TextT> texto = this.repositoryRelational.findById(id);
        this.repositoryCalls.add("getString");
        return texto.isPresent() ? texto.get().getTextValue() : "Texto no encontrado!";
    }

    public Optional<TextT> getText(final Integer id){
        this.repositoryCalls.add("getText");
        return this.repositoryRelational.findById(id);
    }

}
