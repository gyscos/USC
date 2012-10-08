package com.threewisedroids.usc.network;

import java.util.ArrayList;
import java.util.List;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import com.helper.network.json.JSONHandler;
import com.helper.network.json.rpc.JSONRpcHandler;
import com.helper.network.json.JSONServer;
import com.threewisedroids.usc.USC;
import com.threewisedroids.usc.USCParam;

public class USCServer extends JSONServer {

    class USCJSONHandler extends JSONRpcHandler {

        @Override
        public Object getResult(String method, Object params) {
            try {
                if (method.equals("call"))
                    return call((JSONArray) params);
                else if (method.equals("list"))
                    return usc.toJson();
            } catch (JSONException e) {
                e.printStackTrace();
            }

            return null;
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

            return result;
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
