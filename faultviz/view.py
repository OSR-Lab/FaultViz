
from deephaven_server import Server
from deephaven_ipywidgets import DeephavenWidget

import logging 
from IPython.display import display
import pandas as pd
import pygwalker as pyg


_server = None

def start_view_service(port=12345):
    global _server
    global input_table, empty_table, read_csv, agg, _server, dht, _typemap
    Server(port=port, jvm_args=["-Xmx2g", "-DAuthHandlers=io.deephaven.auth.AnonymousAuthenticationHandler"]).start()
    _server = True
    from deephaven import input_table
    from deephaven import empty_table
    from deephaven import dtypes as dht
    from deephaven import agg as agg
    


    _typemap = {int:dht.int64, float:dht.float64, str:dht.string}
    


_typestrmap = {int:'(long)', float:'(double)', str:'(String)'}

def _check_columns(columns:dict, **kwargs):
    logger = logging.getLogger(__name__)
    if len(columns) == 0:
        for v in kwargs.values():
            if not isinstance(v, (int, float, str)):
                return False
        return True
    else:
        if not len(columns) == len(kwargs):
            return False
        for k in kwargs:
            if not k in columns:
                return False
            if not _typemap[type(kwargs[k])] == columns[k]:
                return False
        return True
    
                

class ViewWidget:
    def __init__(self):
        self.table = None
        self._column = {}
        self.logger = logging.getLogger(__name__)
        if _server is None:
            self.logger.error("should run start_view_service before view.")
    
    def update(self, **kwargs):
        """update table only support int, float and str type.
        """
        if self.table is None:
            if not _check_columns(self._column, **kwargs):
                self.logger.error("only support int, float and str to be record!")
                return
            else:
                for k in kwargs:
                    self._column[k] = _typemap[type(kwargs[k])]
                self.table = input_table(col_defs=self._column)
        else:
            if not _check_columns(self._column, **kwargs):
                self.logger.error("record types or name mismatch!")
        
        u = []
        for k in kwargs:
            s = f"%s = %skwargs[`%s`]" % (k, _typestrmap[type(kwargs[k])], k)
            u.append(s)
        
        self.logger.debug(u)
        self.logger.debug(kwargs)
        t = empty_table(1).update(u)
        self.table.add(t)
    
    def show(self, state:str='state'):
        if self.table is None:
            self.logger.info("No data recorded.")
            return
        if state in self._column:
            count_table = self.table.count_by("count", by=[state])
            display(DeephavenWidget(count_table, height=150))
        display(DeephavenWidget(self.table.reverse()))
    
    def plot(self, state:str='state'):
        from deephaven import pandas as dhpd
        if self.table is None:
            self.logger.info("No data recorded.")
            return
        df = dhpd.to_pandas(self.table)
        pyg.walk(df)
        

def csvview(csv:str, state:str='state'):
    logger = logging.getLogger(__name__)
    if _server is None:
        logger.error("should run start_view_service before view.")
        return
    from deephaven import read_csv
    table = read_csv(csv)
    if table.has_columns(state):
        count_table = table.count_by("count", by=[state])
        display(DeephavenWidget(count_table, height=150))
    display(DeephavenWidget(table.reverse()))


def csvplot(name:str):
    df = pd.read_csv(name)
    pyg.walk(df)