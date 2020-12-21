# Wrenchboat

<details>
<summary>
Creating Confing
</summary>

To start create a file called `config.yaml` in the [src](https://github.com/Wrenchs/Wrench/tree/master/src) directory. 

There is some **required** points you must add, and some optional. You can follow the basic scaffold below.
```yaml
token: "your bot's token here"
prefixes: 
 - "main prefix"
devs:
 - 000000000000000000 # Or your id. This is not needed.
plugins:
 - "jishaku"
```

To add more prefixes add `- "prefix here"` on a new line for each prefix.  
To add more devs add `- <id>` on a new line for each dev.
</details>