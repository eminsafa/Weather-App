from datetime import datetime


def open_weather_map_interface(api_function):
    def wrap(*args, **kwargs):
        response = api_function(*args, **kwargs)

        # If error occurred, interface will be passed.
        if 'error' in response.keys():
            return response
        return modify_list(response)

    def modify_list(data):
        # This function modifies two key:
        # 1. Keys starting with digit
        #       Django templates are not supporting keys starting with digit.
        #       This function adds 'new_' prefix to these keys.
        # 2. Timestamps
        #       This function turns timestamps into datetime objects.

        for k, v in data.copy().items():
            if type(v) == dict:
                data[k] = modify_list(v)
            if type(v) == list:
                for i in v:
                    modify_list(i)
            if k[0].isdigit():
                data['new_' + k] = data.pop(k)

        if 'dt' in data.keys():
            dt = datetime.fromtimestamp(data['dt'])
            data['datetime'] = dt
            data['formatted_date'] = dt.strftime('%d %b, %A')

        return data

    return wrap
