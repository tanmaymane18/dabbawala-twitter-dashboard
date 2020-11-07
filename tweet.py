import twint
c = twint.Config()
c.Search = "mumbai dabbawala"
c.Output = "dabbawala_geo_location.csv"
c.Store_csv=True
c.Lang = "en"
c.Since = "2006-03-01"
c.Until = "2020-11-05"
c.Location = True
#c.Near = "Mumbai "
twint.run.Search(c)
