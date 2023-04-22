package com.master.naxer.repositorios.entity.documents;

import org.springframework.data.mongodb.core.mapping.DBRef;
import org.springframework.data.mongodb.core.mapping.Document;

import java.io.Serializable;
import java.util.List;

@Document(collection = "text_t")
public class TextT implements Serializable {

    private final Integer id;
    private final String textValue;
    private final String application;
    private final Integer textType;
    @DBRef
    private final List<TextPropertiesT> textProperties;

    public TextT(Integer id, String textValue, String application, Integer textType, List<TextPropertiesT> textProperties) {
        this.id = id;
        this.textValue = textValue;
        this.application = application;
        this.textType = textType;
        this.textProperties = textProperties;
    }

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
