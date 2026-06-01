package com.hermes;

import burp.api.montoya.MontoyaApi;

public class BurpExtension implements burp.api.montoya.BurpExtension {
    @Override
    public void initialize(MontoyaApi api) {
        api.extension().setName("Hermes Security Insights");

        HermesSyncController controller = new HermesSyncController(api);
        api.userInterface().registerSuiteTab("Hermes Insights", controller.ui());

        controller.start();
        api.logging().logToOutput("Hermes Security Insights initialized. Auto-sync is ON.");
    }
}
