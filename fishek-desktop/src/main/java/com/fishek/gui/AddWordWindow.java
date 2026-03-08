package com.fishek.gui;

import com.fishek.google.SheetsService;

import javax.swing.*;
import java.awt.*;
import java.util.Objects;

public class AddWordWindow {

    public static void show(String text) {
        Font font = new Font("Segoe UI", Font.PLAIN, 30);
        UIManager.put("ComboBox.font", font);
        UIManager.put("TextArea.font", font);
        UIManager.put("Button.font", font);

        JFrame frame = new JFrame("Add to fishek");
        frame.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);

        JComboBox<String> lang = new JComboBox<>(new String[]{
                "ENGLISH", "FRENCH", "RUSSIAN"
        });

        JTextArea area = new JTextArea(text);
        area.setLineWrap(true);
        area.setWrapStyleWord(true);

        JButton send = new JButton("Send");
        send.addActionListener(e -> {
            try {
                SheetsService.append(Objects.requireNonNull(lang.getSelectedItem()).toString(), area.getText());
                frame.dispose();
            } catch (Exception ex) {
                ex.printStackTrace();
            }
        });

        JPanel panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
        panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 10, 10));

        lang.setMaximumSize(new Dimension(Integer.MAX_VALUE, 30));
        panel.add(lang);
        panel.add(Box.createRigidArea(new Dimension(0, 10)));

        JScrollPane scrollPane = new JScrollPane(area);
        scrollPane.setPreferredSize(new Dimension(400, 200));
        panel.add(scrollPane);
        panel.add(Box.createRigidArea(new Dimension(0, 10)));

        send.setAlignmentX(Component.CENTER_ALIGNMENT);
        panel.add(send);

        frame.setContentPane(panel);
        frame.pack();
        frame.setLocationRelativeTo(null);

        frame.setAlwaysOnTop(true);
        frame.toFront();
        frame.requestFocus();

        frame.setVisible(true);
    }
}