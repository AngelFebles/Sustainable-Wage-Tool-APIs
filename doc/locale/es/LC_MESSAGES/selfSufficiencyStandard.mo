��    
      l               �   f   �   U   $  
   z  Q   �     �     �  B  �     .     J  �  i  v   �  `   o     �  Z   �     7     F  b  O     �  9   �   A polars DataFrame with data specific to the County extracted from the Self Sufficiency Standard file. Fetches the Self Sufficiency Standard data from the designated website for Wisconsin. Parameters Reads an Excel file using polars and extracts the Self Sufficiency Standard data. Return type Returns The function scrapes the website to find the most recent Self Sufficiency Standard file link, downloads it if not already present in the './DataFiles' directory, and reads the file to extract data specific to Racine County. The data is processed using the `readFile` function, which reads the file into a Polars DataFrame. The path to the Excel file. selfSufficiencyStandard module Project-Id-Version: sustainable_wage_tool_data 
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
 Un DataFrame de Polars con los datos específicos del Condado extraídos del archivo del Estándar de Autosuficiencia. Recupera los datos del Estándar de Autosuficiencia desde el sitio web designado para Wisconsin. Parámetros Lee un archivo de Excel usando Polars y extrae los datos del Estándar de Autosuficiencia. Tipo de return Devuelve La función raspa el sitio web para encontrar el enlace al archivo más reciente del Estándar de Autosuficiencia, lo descarga si no está presente en el directorio './DataFiles', y lee el archivo para extraer los datos específicos del Condado de Racine. Los datos se procesan usando la función `readFile`, que lee el archivo en un DataFrame de Polars. La ruta al archivo de Excel. Módulo selfSufficiencyStandard (selfSufficiencyStandard) 