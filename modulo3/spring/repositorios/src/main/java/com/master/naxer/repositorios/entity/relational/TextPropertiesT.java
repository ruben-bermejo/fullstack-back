package com.master.naxer.repositorios.entity.relational;

import com.fasterxml.jackson.annotation.JsonIgnore;
import jakarta.persistence.*;

@Entity(name = "Text_Properties_T")
@Table(name = "text_properties_t", schema = "test")
public class TextPropertiesT {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Integer id;
    private Integer textSize;
    private String style;
    private Integer propertyType;
    @ManyToOne(fetch = FetchType.EAGER, optional = false)
    @JoinColumn(name = "text_t_id", referencedColumnName = "id", nullable = false, insertable = false, updatable = false)
    @JsonIgnore
    private TextT textT;

    public Integer getId() {
        return id;
    }

    public Integer getTextSize() {
        return textSize;
    }

    public String getStyle() {
        return style;
    }

    public Integer getPropertyType() {
        return propertyType;
    }

    public TextT getTextT() {
        return textT;
    }
}
