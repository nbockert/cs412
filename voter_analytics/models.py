from django.db import models

# Create your models here.

from datetime import datetime

class Voter(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address_street = models.CharField(max_length=100, blank=True, null=True)
    address_zip = models.CharField(max_length=10, blank=True, null=True)
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=50, blank=True, null=True)
    precinct_number = models.IntegerField(blank=True, null=True)
    
    # Voting participation fields for past elections
    v20state = models.BooleanField(default=False)
    v21town = models.BooleanField(default=False)
    v21primary = models.BooleanField(default=False)
    v22general = models.BooleanField(default=False)
    v23town = models.BooleanField(default=False)
    
    # Score based on voting participation
    voter_score = models.PositiveIntegerField(default=0)

    # def calculate_voter_score(self):
    #     """Calculate voter_score based on the past 5 election participation fields."""
    #     self.voter_score = sum([
    #         self.v20state, self.v21town, self.v21primary,
    #         self.v22general, self.v23town
    #     ])
    #     self.save()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct_number}"

def load_data():
    """Function to load voter data records from CSV file into Django model instances."""
    # First, delete existing records to prevent duplicates
    Voter.objects.all().delete()
    print("Deleted existing records.")
    
    import csv
    from datetime import datetime
    
    filename = '/Users/norabockert/Desktop/newton_voters.csv'
    count = 0
    print("Starting to load data...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        # If you're getting header issues, print headers to check them
        reader = csv.DictReader(f)
        print("CSV Headers:", reader.fieldnames)  # Debugging line
        
        for row in reader:
            try:
                # Debug print first row
                if count == 0:
                    print("First row data:", row)  # Debugging line
                
                # Convert date strings to datetime objects
                dob = datetime.strptime(row['Date of Birth'], '%Y-%m-%d').date()
                reg_date = datetime.strptime(row['Date of Registration'], '%Y-%m-%d').date()
                
                # Convert 'TRUE'/'FALSE' strings to boolean values
                # Using strip() to remove any whitespace and upper() to handle case variations
                v20state = str(row['v20state']).strip().upper() == 'TRUE'
                v21town = str(row['v21town']).strip().upper() == 'TRUE'
                v21primary = str(row['v21primary']).strip().upper() == 'TRUE'
                v22general = str(row['v22general']).strip().upper() == 'TRUE'
                v23town = str(row['v23town']).strip().upper() == 'TRUE'
                
                # Debug print for first row
                if count == 0:
                    print("Parsed election data for first row:")
                    print(f"v20state: {row['v20state']} -> {v20state}")
                    print(f"v21town: {row['v21town']} -> {v21town}")
                    print(f"v21primary: {row['v21primary']} -> {v21primary}")
                    print(f"v22general: {row['v22general']} -> {v22general}")
                    print(f"v23town: {row['v23town']} -> {v23town}")
                
                # Calculate voter score (verifying against the provided score)
                calculated_score = sum([v20state, v21town, v21primary, v22general, v23town])
                provided_score = int(row['voter_score']) if 'voter_score' in row else calculated_score
                
                if count == 0:
                    print(f"Calculated score: {calculated_score}, Provided score: {provided_score}")
                
                voter = Voter(
                    first_name=row['First Name'].strip(),
                    last_name=row['Last Name'].strip(),
                    address_street=row['Residential Address - Street Name'].strip(),
                    address_zip=row['Residential Address - Zip Code'].strip(),
                    date_of_birth=dob,
                    date_of_registration=reg_date,
                    party_affiliation=row['Party Affiliation'].strip(),
                    precinct_number=row['Precinct Number'].strip(),
                    
                    # Store boolean values for election participation
                    v20state=v20state,
                    v21town=v21town,
                    v21primary=v21primary,
                    v22general=v22general,
                    v23town=v23town,
                    
                    # Use calculated score
                    voter_score=calculated_score
                )
                
                voter.save()
                count += 1
                
                if count % 1000 == 0:
                    print(f"Processed {count} records...")
                    
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Error message: {str(e)}")
                continue
    
    print(f'Done. Created {count} Voter records.')