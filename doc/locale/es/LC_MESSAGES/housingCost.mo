��          L               |   Q   }   �   �   `   Y  
  �     �  �  �  Z   g  �   �  }   Z  3  �  *      Prints a message if the request fails, including the status code of the response. Returns: polars.DataFrame: A polars DataFrame with three columns, 'Type', 'Lookup', and 'Cost', representing housing costs for each type. Scrapes the HUD website to retrieve the most recent housing cost data for Racine, WI by default. The function sends a GET request to the HUD API to fetch data for different bedroom sizes. If successful, it processes the JSON response into a Polars DataFrame containing housing costs for Efficiency, One-Bedroom, Two-Bedroom, Three-Bedroom, and Four-Bedroom types. housingCost module Project-Id-Version: sustainable_wage_tool_data 
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2025-01-09 07:16-0600
PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE
Last-Translator: FULL NAME <EMAIL@ADDRESS>
Language: es
Language-Team: es <LL@li.org>
Plural-Forms: nplurals=2; plural=(n != 1);
MIME-Version: 1.0
Content-Type: text/plain; charset=utf-8
Content-Transfer-Encoding: 8bit
Generated-By: Babel 2.16.0
 Imprime un mensaje si la solicitud falla, incluyendo el código de estado de la respuesta. Devuelve: polars.DataFrame: Un DataFrame de Polars con tres columnas, 'Type', 'Lookup' y 'Cost', que representan los costos de vivienda para cada tipo. Extrae datos del sitio web de HUD para obtener los costos de vivienda más recientes para Racine, WI de forma predeterminada. La función envía una solicitud GET a la API de HUD para obtener datos de diferentes tamaños de dormitorio. Si tiene éxito, procesa la respuesta JSON en un DataFrame de Polars que contiene costos de vivienda para tipos de Eficiencia, Un Dormitorio, Dos Dormitorios, Tres Dormitorios y Cuatro Dormitorios. Módulo de costo de vivienda (housingCost) 