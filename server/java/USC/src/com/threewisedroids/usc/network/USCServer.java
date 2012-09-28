package com.threewisedroids.usc.network;

import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.helper.network.NetworkHandler;
import com.helper.network.NetworkServer;
import com.threewisedroids.usc.USC;
import com.threewisedroids.usc.USCParam;

public class USCServer extends NetworkServer {

    class USCNetworkHandler extends NetworkHandler {

        @Override
        public boolean handleMessage(String line) {
            try {
                List<USCParam> params = new ArrayList<USCParam>();

                // The message is a JSON Array.
                // System.out.println(line);
                JSONArray array = new JSONArray(line);
                for (int i = 0; i < array.length(); i++) {
                    JSONArray arg = array.getJSONArray(i);
                    USCParam param = new USCParam(arg.getInt(1),
                            arg.getString(0));

                    params.add(param);
                }

                String answer = usc.handleCommand(params);
                boolean refresh = usc.refresh();

                JSONObject result = new JSONObject();

                result.put("answer", answer);
                result.put("refresh", refresh);
                if (refresh)
                    result.put("root", usc.toJson());

                send(result.toString());
            } catch (JSONException e) {
                e.printStackTrace();
            }
            return false;
        }

        @Override
        public void onConnect(String ip) {
            // Send list of commands
            try {
                JSONObject root = usc.toJson();
                String line = root.toString();
                send(line);
            } catch (JSONException e) {
                e.printStackTrace();
            }
        }

        @Override
        public void onDisconnect() {
        }

    }

    USC usc;

    public USCServer(USC usc) {
        this.usc = usc;
    }

    @Override
    public NetworkHandler getHandler() {
        return new USCNetworkHandler();
    }
}
