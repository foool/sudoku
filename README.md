A simple web page for solving sudoku problems 
---------------------------------------------

environment: XAMPP + python + wsgi_mod + web.py

Add following configuration to you apache configuration:

    <Directory "++full path of web.py without file name++">       
        Order allow,deny   
        Allow from all 
    </Directory> 

    Alias /static "++full path of white.png without file name++" 
    AddType text/html .py

    <Directory "++full path of white.png without file name++">
        Order allow,deny   
        Allow from all 
    </Directory>

    <IfModule wsgi_module>   
        WSGIScriptAlias /sudoku "++full path of web.py without file name++"   
    </IfModule> 
