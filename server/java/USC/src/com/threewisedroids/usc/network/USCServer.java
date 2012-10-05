package com.threewisedroids.usc.network;

import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.helper.network.JSONHandler;
import com.helper.network.JSONServer;
import com.threewisedroids.usc.USC;
import com.threewisedroids.usc.USCParam;

public class USCServer extends JSONServer {

    class USCJSONHandler implements JSONHandler {

        @Override
        public JSONObject getAnswer(JSONObject command) {


            try {

                String method = command.getString("method");
                if (method.equals("call"))
                    return call(command.getJSONArray("params"));
                else if (method.equals("list"))
                    return list();
            } catch (JSONException e) {
                e.printStackTrace();
            }

            return null;
        }

        public JSONObject list() throws JSONException {
            JSONObject result = new JSONObject();
            result.put("result", usc.toJson());
            return result;
        }

        public JSONObject call(JSONArray array) throws JSONException {

            List<USCParam> params = new ArrayList<USCParam>();

            // The message is a JSON Array.
            // System.out.println(line);
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

            JSONObject obj = new JSONObject();

            obj.put("result", result);

            return obj;
        }
    }

    USC usc;

    public USCServer(USC usc) {
        this.usc = usc;
    }

    @Override
    public JSONHandler getHandler() {
        return new USCJSONHandler();
    }
}
