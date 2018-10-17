"""
    Sdmc User model.
    This object is defined in https://sds.stormshieldcs.eu/doc/api/#tag/Users
"""
class UserData:
    def __init__(self, oneUser):
        self.id =  oneUser['id']
        self.roles =  oneUser['roles']
        self.devices_count = oneUser['devices_count']
        self.state =  oneUser['state']
        self.first_name =  oneUser['first_name']
        self.last_name =  oneUser['last_name']
        self.email =  oneUser['email']
        self.last_activity_date =  oneUser['last_activity_date']
        self.register_date =  oneUser['register_date']

    def getValueByName(self,attribute):
        """ Get attribute value by name
        Input:
           attribute: attribute name
        return : attribute value as string
        """
        try:
            value = getattr(self,attribute);
            if isinstance(value, list):
                value = ','.join(value)
            elif isinstance(value, int):
                value = str(value)
            return value
        except:
            raise Exception('An error occured! -> column {} does not exist!'.format(attribute))

    def toCsv(self, exposedData):
        """ Get UserData values as an array
        Input:
           exposedData: name of attributes to retrieve
        return : array containing all selected values
        """
        values=[]
        for attribute in exposedData:
            values.append(self.getValueByName(attribute))
        return values

    @staticmethod
    def getAttributeName():
        """ Getter all UserData attribute name
        return : array containing all userData attribute names
        """
        return ['id', 'first_name', 'last_name', 'email', 'state','roles', 'devices_count', 'last_activity_date', 'register_date']
