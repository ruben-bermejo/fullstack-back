package com.master.naxer.repositorios.repository.relational;

import com.master.naxer.repositorios.entity.relational.TextT;
import io.micrometer.core.annotation.Timed;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
@Timed(value = "time.repository.relational", description = "controlando el tiempo al realizar consultas")
public interface TextRepositoryRelational extends JpaRepository<TextT, Integer> {
}
