package com.fishek.util;

import java.awt.*;
import java.awt.datatransfer.DataFlavor;

public class ClipboardUtil {

    public static String getText() {
        try {
            return (String) Toolkit.getDefaultToolkit()
                    .getSystemClipboard()
                    .getData(DataFlavor.stringFlavor);
        } catch (Exception e) {
            return "";
        }
    }
}
