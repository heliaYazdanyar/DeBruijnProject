import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data=[['Algo', '0',121],['Obl','0',121],['Opt','0',117],
['Algo', '0.15', 103],['Obl','0.15',114],['Opt','0.15',117],
['Algo', '0.3',85],['Obl','0.3',121],['Opt','0.15',116],
['Algo','0.45',67],['Obl','0.45',121],['Opt','0.15',115],
['Algo','0.6',49],['Obl','0.6',121],['Opt','0.15',114],
['Algo','0.75',31],['Obl','0.75',121],['Opt','0.75',111],
['Algo','0.9',12],['Obl','0.9',121],['Opt','0.9',107]
]

df=pd.DataFrame(data,columns=['name','temp_p','cost'])

print(df)

# plot with seaborn and use the hue parameter
plt.figure(figsize=(10, 6))
fs = 20
sns.lineplot(x='temp_p', y='cost', data=df, hue='name')
plt.legend(bbox_to_anchor=(0.25, 0), loc='lower right', fontsize=fs)
plt.ylabel('Access Cost', fontsize=fs)
plt.xlabel('Temporal Locality', fontsize=fs)
plt.tick_params(axis='both', which='major', labelsize=fs)
plt.savefig("on_off_lines_temp-acc.pdf",bbox_inches='tight')
plt.show()