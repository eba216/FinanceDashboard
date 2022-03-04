

function update_graph_data(id, src, stock_name)
{
    $.getJSON(
        src,
        {"stock": stock_name},
        function(data)
        {
            $("#" + id).html(data.result);
        }
    );
};

function update_live_data(id, src, stock_name){
    update_graph_data(id, src, stock_name);
    setInterval(update_graph_data, 60000, id, src, stock_name); 
}
