.. _how_to_guides__validation__how_to_trigger_email_as_a_validation_action:

How to trigger Email as a Validation Action
=========================================================

This guide will help you trigger emails as a :ref:`Validation Action <validation_actions>`
.  It will allow you to send an email including information about a Validation Result, including whether or not the Validation succeeded.

.. admonition:: Prerequisites: This how-to guide assumes that you have already:

    - Configured an email account on the SMTP server you are going to use to send the email
    - Identified the email addresses that messages will be sent to.

Steps
-----

1. Open ``uncommitted/config_variables.yml`` file and add the following variables by adding the following lines:

.. code-block:: yaml

    smtp_address: [address of the smtp server]
    smtp_port: [port used by the smtp server]
    sender_login: [login used to send the email]
    sender_password: [password used to send the email]
    sender_alias: [optional alias used to send the email (default = sender_login)]
    receiver_emails: [addresses you want to send the email to]  # each address must be separated by commas


2. Open ``great_expectations.yml`` and add ``send_email_on_validation_result`` action to ``validation_operators``. Make sure the following section exists in the ``great_expectations.yml`` file.

.. code-block:: yaml

    validation_operators:
        action_list_operator:
            # To learn how to configure sending emails during evaluation
            # (and other customizations), read: https://docs.greatexpectations.io/en/latest/reference/validation_operators/action_list_validation_operator.html
            class_name: ActionListValidationOperator
            action_list:
            #--------------------------------
            # here is what you will be adding
            #--------------------------------
            - name: send_email_on_validation_result # name can be set to any value
              action:
                class_name: EmailAction
                notify_on: all # possible values: "all", "failure", "success"
                notify_with: # optional list containing the DataDocs sites to include in the notification. Defaults to including links to all configured sites.
                # You can choose between using SSL encryption, TLS encryption or none of them (not advised)
                use_tls: False
                use_ssl: True
                renderer:
                  module_name: great_expectations.render.renderer.email_renderer
                  class_name: EmailRenderer
                # put the actual following information in the uncommitted/config_variables.yml file
                # or pass in as environment variable
                smtp_address: ${smtp_address}
                smtp_port: ${smtp_port}
                sender_login: ${sender_login}
                sender_password: ${sender_password}
                sender_alias: ${sender_alias}
                receiver_emails: ${receiver_emails}  # string containing email addresses separated by commas

3. Run your ``action_list_operator``, to validate a batch of data and receive an email on the success or failure of validation suite.  

  .. code-block:: python
  
      context.run_validation_operator('action_list_operator', assets_to_validate=batch, run_name="email_test")

  If successful, you should receive an email that looks like this:

    .. image:: /images/email_example.png


Additional notes
--------------------

- If your ``great_expectations.yml`` contains multiple configurations for Data Docs sites, all of them will be included in the email by default. If you would like to be more specific, you can configure the ``notify_with`` variable in your ``great_expectations.yml``.
- The following example will configure the email to include links Data Docs at ``local_site`` and ``s3_site``.

.. code-block:: yaml

    # Example data_docs_sites configuration
    data_docs_sites:
      local_site:
        class_name: SiteBuilder
        show_how_to_buttons: true
        store_backend:
          class_name: TupleFilesystemStoreBackend
          base_directory: uncommitted/data_docs/local_site/
        site_index_builder:
          class_name: DefaultSiteIndexBuilder
      s3_site:  # this is a user-selected name - you may select your own
        class_name: SiteBuilder
        store_backend:
          class_name: TupleS3StoreBackend
          bucket: data-docs.my_org  # UPDATE the bucket name here to match the bucket you configured above.
        site_index_builder:
          class_name: DefaultSiteIndexBuilder
          show_cta_footer: true

    validation_operators:
        action_list_operator:
        ...
        - name: send_email_on_validation_result # name can be set to any value
              action:
                class_name: EmailAction
                notify_on: all # possible values: "all", "failure", "success"
                #--------------------------------
                # This is what was configured
                #--------------------------------
                notify_with:
                  - local_site
                  - gcs_site
                use_ssl: True
                use_tls: False
                renderer:
                  module_name: great_expectations.render.renderer.email_renderer
                  class_name: EmailRenderer
                # put the actual following information in the uncommitted/config_variables.yml file
                # or pass in as environment variable
                smtp_address: ${smtp_address}
                smtp_port: ${smtp_port}
                sender_login: ${sender_login}
                sender_password: ${sender_password}
                sender_alias: ${sender_alias}
                receiver_emails: ${receiver_emails} # string containing email addresses separated by commas


Additional resources
--------------------

- The EmailAction uses smtplib. You can get more information about this module `here <https://docs.python.org/3/library/smtplib.html>`_.

.. discourse::
    :topic_identifier: 234
