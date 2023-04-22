package com.master.naxer.repositorios.entity.documents;

import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.io.Serializable;

@Document(collection = "text_properties_t")
public class TextPropertiesT implements Serializable {

    @Id
    private final Integer id;
    private final Integer size;
    private final String style;
    private final Integer propertyType;

    public TextPropertiesT(Integer id, Integer size, String style, Integer propertyType) {
        this.id = id;
        this.size = size;
        this.style = style;
        this.propertyType = propertyType;
    }

    public Integer getId() {
        return id;
    }

    public Integer getSize() {
        return size;
    }

    public String getStyle() {
        return style;
    }

    public Integer getPropertyType() {
        return propertyType;
    }
}
