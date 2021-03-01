def add_variable(data, function, var_name):
    data[var_name] = data['signal'].apply(function)
