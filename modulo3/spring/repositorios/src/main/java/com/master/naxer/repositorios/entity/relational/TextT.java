package com.master.naxer.repositorios.entity.relational;

import jakarta.persistence.*;

import java.util.List;

@Entity(name = "Text_t")
@Table(name = "text_t", schema = "test")
public class TextT {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Integer id;
    private String textValue;
    private String application;
    private Integer textType;
    @OneToMany(fetch = FetchType.EAGER, mappedBy = "textT", cascade = CascadeType.ALL)
    private List<TextPropertiesT> textProperties;

    public Integer getId() {
        return id;
    }

    public String getTextValue() {
        return textValue;
    }

    public String getApplication() {
        return application;
    }

    public Integer getTextType() {
        return textType;
    }

    public List<TextPropertiesT> getTextProperties() {
        return textProperties;
    }
}
