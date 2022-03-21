Warning, Strategies in this folder do have a lookahead bias.

Please see these as practice to see if you can spot the lookahead bias.


<details>
<summary>Expand for spoilers / solution</summary>

Please Click on each strategy to see details of the mistakes.

<details>
<summary>DevilStra</summary>

`normalize()` uses `.min()` and `.max()`. This uses the full dataframe, not just past data.

</details>

<details>
<summary>GodStraNew</summary>

`normalize()` uses `.min()` and `.max()`. This uses the full dataframe, not just past data.
</details>
<details>
<summary>Zeus</summary>

uses `.min()` and `.max()` to normalize `trend_ichimoku_base` as well as `trend_kst_diff`.

</details>

<details>
<summary>wtc</summary>

``` python
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
```

Using a MinMaxScaler will automatically take the absolute maximum and minimum of a series.

</details>
</details>

</details>
