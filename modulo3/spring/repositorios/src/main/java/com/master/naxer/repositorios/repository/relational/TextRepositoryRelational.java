package com.master.naxer.repositorios.repository.relational;

import com.master.naxer.repositorios.entity.relational.TextT;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface TextRepositoryRelational extends JpaRepository<TextT, Integer> {
}
