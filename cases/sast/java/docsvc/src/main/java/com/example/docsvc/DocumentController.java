package com.example.docsvc;

import java.io.ByteArrayInputStream;
import java.io.ObjectInputStream;
import java.util.Base64;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;

import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.w3c.dom.Document;

@RestController
public class DocumentController {

    // Parse an uploaded XML document and return its root element name.
    @PostMapping("/documents/parse")
    public String parse(@RequestBody String xml) throws Exception {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
        DocumentBuilder builder = factory.newDocumentBuilder();
        Document doc = builder.parse(new ByteArrayInputStream(xml.getBytes()));
        return doc.getDocumentElement().getNodeName();
    }

    // Restore a previously exported document state from a client token.
    @PostMapping("/documents/restore")
    public Object restore(@RequestBody String token) throws Exception {
        byte[] data = Base64.getDecoder().decode(token);
        ObjectInputStream ois = new ObjectInputStream(new ByteArrayInputStream(data));
        return ois.readObject();
    }
}
