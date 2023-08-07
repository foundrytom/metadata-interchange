# Commented imports are illustrative and may not exist yet
from openassetio_mediacreation.traits.managementPolicy import (
    ManagedTrait, ResolvesFutureEntitiesTrait
)
from openassetio_mediacreation.specifications.files import (
    # TextFileSpecification
)


# As ever, an appropriately configured context is required
context = manager.createContext()
context.access = context.kWrite

# The first step is to see if the manager wants to manage text files
policy = manager.managementPolicy([TextFileSpecification.kTraitSet], context)[0]

if not ManagedTrait.isImbuedTo(policy):
  # The manager doesn't care about this type of asset
  return

# Not all managers can tell us where to put files (irksome).
# The reality of handling this is somewhat more challenging, and
# depends on the nature of the task in hand. One for further discussion.
save_path = os.path.join(os.path.expanduser('~'), 'greeting.txt')
encoding = "utf-8"

# Whenever we make new data, we always tell the manager first,
# This allows it to create a placeholder version or similar.
# NOTE: It is critical to always use the working_ref from now on.
working_ref = manager.preflight(
        entity_ref, TextFileSpecification.kTraitSet, context)

# We then check if the manager can tell us where to save the file.
if ResolvesFutureEntitiesTrait.isImbuedTo(policy):
    working_data = manager.resolve(
            working_ref, TextFileSpecification.kTraitSet, context)
    working_spec = TextFileSpecification(working_data)
    if save_url := working_spec.locatableContentTrait().getLocation():
        save_path = pathFromURL(save_url)  # URL decode etc
    if custom_encoding := working_spec.textEncodingTrait().getEncoding():
        encoding = custom_encoding

# Now we can write the file
with open(save_path, 'w', encoding=encoding) as f:
   f.write("Hello from the documentation example\n")

# Prepare the entity specification to register, with the data about
# where we actually wrote the data to, and with what encoding.
file_spec = TextFileSpecification.create()
file_spec.locatableContentTrait().setLocation(pathToURL(save_path))
file_spec.textEncodingTrait().setEncoding(encoding)

# Now the data has been written, we register the file and the publish
# is complete. Update the context retention to denote that we're going
# to save a reference to this entity in our user's history.
context.retention = context.kPermanent
final_ref = manager.register(working_ref, file_spec.traitsData(), context)

# We can persist this reference as we used the kPermanent retention
with open(os.path.join(os.path.expanduser('~'), 'history', 'a') as f:
    f.write(f"{final_ref}\n")