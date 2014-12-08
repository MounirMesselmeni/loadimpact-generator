#Create virtualenv
virtualenv --no-site-packages loadimpact_env
cd loadimpact_env
source bin/activate
git clone https://github.com/MounirMesselmeni/loadimpact-generator.git
cd loadimpact-generator

#Install requirement
pip install -r requirements.txt

# Run generator
python generate_li_config.py
Provide your API_TOKEN tp upload user scenario, test config and running the test
