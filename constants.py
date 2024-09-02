# Authentication
TBNB_ID = "26d7d9cf-6bcb-4317-afd0-c0bdf30d2014"
BEARER_TOKEN = ("Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiODdlZDU5NmIyOGQ3ZWQxNmUyMTU0Y2Jk"
                "Mzk5YzFiMDljZDdjN2Q2OGVhZGZlNjg5ODk5Yzc5ZGNkZDc3YzI3MGZmNjVlOWRkNzJlNDBhYjkiLCJpYXQiOjE3MjQwMDI2NzkuN"
                "DAxNTAzLCJuYmYiOjE3MjQwMDI2NzkuNDAxNTA4LCJleHAiOjQ4NDgwNTM4NzkuMzk1NTA1LCJzdWIiOiI1MDk2MjkiLCJzY29wZX"
                "MiOltdfQ.JUQILJQ69CaQmbAoUT78KhADlvMhDxUTIzhR0JoHpd7R5YCgUNM6-zfily-X4-BFFY8aM0cDEcPNnJ8OrgRRCsk-WxHH"
                "dQyZ2HWUfs6zLgse_-hlw54LXu7r4w61gMEhdoNQJYkU8K3PUNCygJ5sn-Gj7NqMr9c662HWUDlTYuCH7gsCgbaMUtgzAnaMjr_j8"
                "rK7ALM2F5hxnyqA0C7zvuyJnXvAPIUwoQT8AXEcWKb3tfLx5e2nir1i0PiViHKBbzmynGZb0b0T1ErnUEpqzlUaa4MXMrkLFSscvW"
                "nT5QJld3o3UTyu6v7fFAQXxpyi7uYm1cFV_z-Sb6DUNIJKdSOuvh55qE-4gXFW6PLWHKKNLOneG54Ioxl907swlkY_7x7xzNKAejL"
                "cPnYuXgcWNaLlTV7xQ5zlMD5qfbZofZjff5T2JAzFxeFiovozPusfQukTbAc6CZFW6pd3maxTB-zr0wFvJ7rLEpQS_Ucp8JiS0UDA"
                "0nmi4Uz_PD9AjyCLO1neSXdEIucnyA1fJCWLzbXb9BfV-kzqsfu3R7GlkaNmgG-__vNyxxm07aHcmi_P0A8jA6cnT73jXjq6DRrok"
                "WmmBNZ8qcum9euzJoD9isZ-pbMZYQoQFw7FDka-Db-qYEuLnPVhwSiW6W3Gw2wmGclt6QWFGS9KDgtSMrjih24")
ACCOUNT_SID = "AC556bd0c68b1a5edafa21078f4962ba4c"
# Messages
SCHEDULE_WASHBAR = ("\n\nWashBar : Le WashBar se situe au au : 39 Rue Ausone, 33000, Bordeaux. Attention : Le WashBar "
                    "est fermé le samedi, ainsi que le dimanche jusqu'à 15h.")
MESSAGE_PUT_TAKE_FRIDAY = (", vous devez aller déposer le linge après votre ménage, à la laverie partenaire "
                           "WashBar, et le récupérer aujourd'hui. " + SCHEDULE_WASHBAR)
MESSAGE_PUT_TAKE_BEFORE_SATURDAY = (", vous devez aller déposer le linge après votre ménage, à la laverie partenaire "
                                    "WashBar. N'oubliez pas d'aller récupérer le linge avant samedi prochain. "
                                    + SCHEDULE_WASHBAR)
MESSAGE_TAKE_HOME_LAUNDRY = (", vous devez aller déposer le linge jeudi au plus tard, à la laverie partenaire WashBar,"
                             " et le récupérer au plus tard pour vendredi pour la prochaine réservation. "
                             "\nAttention : Vous ne pouvez pas déposer le linge aujourd'hui." + SCHEDULE_WASHBAR)
MESSAGE_TAKE_HOME_LAUNDRY_SUNDAY = (", vous devez aller déposer le linge jeudi au plus tard, à la laverie partenaire "
                                    "WashBar, et le récupérer au plus tard pour vendredi pour la prochaine "
                                    "réservation.\nAttention : Vous pouvez déposer le linge aujourd'hui à partir de "
                                    "15h." + SCHEDULE_WASHBAR)
MESSAGE_TAKE_LINGE_FRIDAY = (", vous devez aller déposer le linge à la laverie partenaire WashBar et"
                             " le récupérer au plus tard vendredi." + SCHEDULE_WASHBAR)
MESSAGE_PUT_LINGE_SUNDAY = (", vous devez aller déposer le linge sale dimanche, à partir de 15h et le récupérer au "
                            "plus tard vendredi, à la laverie partenaire WashBar." + SCHEDULE_WASHBAR)
MESSAGE_PUT_LAUNDRY = (", vous devez aller déposer le linge sale, à la laverie partenaire WashBar, et le récupérer au "
                       "plus tard vendredi." + SCHEDULE_WASHBAR)
MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY = (", vous devez aller déposer le linge sale, à la laverie partenaire WashBar, et le "
                                   "récupérer vendredi, car une réservation à lieu le jour même." + SCHEDULE_WASHBAR)
MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY_2 = (", vous devez aller déposer le linge sale, à la laverie partenaire WashBar, et le "
                                     "récupérer vendredi prochain au plus tard.\nAttention : Vous ne pouvez pas déposer"
                                     " le linge samedi." + SCHEDULE_WASHBAR)
MESSAGE_PUT_LAUNDRY_TAKE_FRIDAY_NEXT = (", vous devez aller déposer le linge sale, à la laverie partenaire WashBar, et "
                                        "le récupérer vendredi, car une réservation à lieu le samedi suivant et le "
                                        "le WashBar sera fermé." + SCHEDULE_WASHBAR)
MESSAGE_PUT_LAUNDRY_TAKE_THURSDAY_SUNDAY = (", vous devez aller déposer le linge sale, à la laverie partenaire WashBar,"
                                            " jeudi prochain au plus tard et le récupérer vendredi.\nAttention : Vous "
                                            "ne pouvez pas déposer le linge aujourd'hui." + SCHEDULE_WASHBAR)
MESSAGE_PUT_LAUNDRY_TAKE_THURSDAY = (", vous devez aller déposer le linge sale, à la laverie partenaire WashBar, jeudi"
                                     " prochain au plus tard et le récupérer vendredi." + SCHEDULE_WASHBAR)
MESSAGE_CHECK_FORM = ", n'oubliez pas de remplir le formulaire pour le linge sale."
