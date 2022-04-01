NUMSLOTPARAMS=$(printenv CONDA_SHLVL)
if [ ! $NUMSLOTPARAMS ]; then
  echo "Your slot case is default"
else
  echo "NUMSLOTPARAMS=$NUMSLOTPARAMS"
  python /home/Frank_Tung/Desktop/ChangeXmlContent/change_oam_sysrepo_du_params.py --slot $NUMSLOTPARAMS
fi

