package com.threewisedroids.usc;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.threewisedroids.usc.network.USCServer;

/**
 * USC : Universal Server Controller.
 * Server-side
 * 
 * It is actually a Command Tree.
 * Sends command list on connection, and on command result when required.
 * 
 */
public class USC {

    public static class USCList {
        List<USCNode> nodes = new ArrayList<USCNode>();

        public USCList item(String name) {
            return item(name, -1);
        }

        public USCList item(String name, int commandId, String... childs) {
            nodes.add(new USCNode(name, commandId, childs));
            return this;
        }

        public JSONObject toJson() throws JSONException {
            JSONObject result = new JSONObject();

            for (USCNode node : nodes) {
                JSONArray childs = new JSONArray();
                for (String child : node.childs)
                    childs.put(child);

                JSONArray array = new JSONArray();
                array.put(node.commandId);
                array.put(childs);

                result.put(node.name, array);
            }

            return result;
        }
    }

    public static class USCNode {
        String       name;
        int          commandId;
        List<String> childs;

        USCNode(String name, int commandId, String... childs) {
            this.name = name;
            this.commandId = commandId;
            this.childs = Arrays.asList(childs);
        }
    }

    public static void main(String[] args) {
        final int id_start = 0, id_stop = 1;

        USC usc = new USC(new USCHandler() {

            @Override
            public String handleCommand(List<USCParam> params) {
                if (params.isEmpty())
                    return "Empty command";

                switch (params.get(0).commandId) {
                    case id_start:
                        System.out.println("Starting server !");
                        return "Starting...";
                    case id_stop:
                        System.out.println("Stoping server !");
                        return "Stoping...";
                }

                return "Unknown Error.";
            }
        });

        usc.list("entry").item("start", id_start, "number")
                .item("stop", id_stop);
        usc.list("number");

        usc.start(1111);

    }

    USCServer                server         = new USCServer(this);

    USCHandler               handler;

    HashMap<String, USCList> lists          = new HashMap<String, USCList>();

    boolean                  refresh_needed = false;

    public USC(USCHandler handler) {
        this.handler = handler;
    }

    public String handleCommand(List<USCParam> params) {
        if (params == null || params.isEmpty())
            return "Empty command";

        if (handler != null)
            return handler.handleCommand(params);
        return "";
    }

    public USCList list(String name) {
        if (!lists.containsKey(name))
            lists.put(name, new USCList());
        return lists.get(name);
    }

    public void needRefresh() {
        refresh_needed = true;
    }

    public boolean refresh() {
        boolean result = refresh_needed;
        refresh_needed = false;
        return result;
    }

    public void start(int port) {
        server.listen(port);
    }

    public void stop() {
        server.close();
    }

    public JSONObject toJson() throws JSONException {
        JSONObject result = new JSONObject();

        for (String name : lists.keySet())
            result.put(name, lists.get(name).toJson());

        return result;
    }

}
