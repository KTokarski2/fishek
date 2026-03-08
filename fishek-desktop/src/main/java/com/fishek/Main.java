package com.fishek;

import com.fishek.util.GlobalHotkey;

public class Main {
    public static void main(String[] args) throws Exception {
        System.out.println("Fishek desktop started");
        GlobalHotkey.register();
        while (true) {
            Thread.sleep(1000);
        }
    }
}