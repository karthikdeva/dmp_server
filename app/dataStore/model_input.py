import graphene


class CitizenInput(graphene.InputObjectType):
    id = graphene.ID()
    citizenId = graphene.ID()
    name = graphene.String()
    mobile1 = graphene.String()
    mobile2 = graphene.String()
    doorNumber = graphene.String()
    AadhaarNumber = graphene.String()
    nameOnNamePlate = graphene.String()
    geoLocation = graphene.String()
    street = graphene.String()
    locality = graphene.String()
    area = graphene.String()
    noOneAtHome = graphene.Boolean()
    createdBy = graphene.ID()

