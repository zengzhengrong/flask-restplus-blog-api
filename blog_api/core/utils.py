

class CreateApiModel(object):
    '''
    parm api, namespace  
    parm model, parent model  
    parm name, the new api name  
    parm remove_list = None  
    parm add = {}  
    '''
    
    def __init__(self, api,model,name,remove_list=None,add={}):
        self.api = api
        self.model = model
        self.name = name
        self.remove_list = remove_list
        self.add = add

    def inherit(self):
        new_model = self.api.inherit(self.name,self.model)
        return new_model
     
    
    def inherit_remove(self,remove_list):
        self.remove_list = remove_list
        if self.remove_list:
            new_model = self.inherit()
            for k in self.remove_list:
                del new_model[k]
            return new_model
        else:
            raise AttributeError('Remove fields fail ')
    
    def inherit_add(self,add,internal_model=None):
        self.add = add
        if self.add:
            new_model = self.inherit()
            for k,w in self.add:
                new_model[k] = w
            return new_model
        else:
            raise AttributeError('Add fields fail ')
    
    def inherit_ra(self,remove_list,add):
        rm_model = self.inherit_remove(remove_list)
        new_model = self.inherit_add(add,internal_model=rm_model)
        return new_model



        
    