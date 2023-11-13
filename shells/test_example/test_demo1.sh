curl --location 'http://172.29.186.21:8555/nlp_term_attr_classifier' \
--header 'Content-Type: application/json' \
--data '{
  "term_list": [
    {
      "name": "Use Patent Claims",
      "text": "The Licensor grants to the Licensee royalty-free, non-exclusive usage rights to any patents held by the Licensor, to the extent necessary to make use of the rights granted on the Work under this Licence."
    },
    {
      "name": "Use Trademark",
      "text": "under intellectual property rights (other than patent or trademark) Licensable by Initial Developer"
    }
  ]
}'