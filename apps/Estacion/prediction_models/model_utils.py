import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import json

#### Data windowing
class WindowGenerator():
  def __init__(self, input_width, label_width, shift,
               train_df=train_df, val_df=val_df, test_df=test_df,
               label_columns=None):
    # Store the raw data.
    self.train_df = train_df
    self.val_df = val_df
    self.test_df = test_df

    # Work out the label column indices.
    self.label_columns = label_columns
    if label_columns is not None:
      self.label_columns_indices = {name: i for i, name in
                                    enumerate(label_columns)}
    self.column_indices = {name: i for i, name in
                           enumerate(train_df.columns)}

    # Work out the window parameters.
    self.input_width = input_width
    self.label_width = label_width
    self.shift = shift

    self.total_window_size = input_width + shift

    self.input_slice = slice(0, input_width)
    self.input_indices = np.arange(self.total_window_size)[self.input_slice]

    self.label_start = self.total_window_size - self.label_width
    self.labels_slice = slice(self.label_start, None)
    self.label_indices = np.arange(self.total_window_size)[self.labels_slice]

  def __repr__(self):
    return '\n'.join([
        f'Total window size: {self.total_window_size}',
        f'Input indices: {self.input_indices}',
        f'Label indices: {self.label_indices}',
        f'Label column name(s): {self.label_columns}'])

### Split window
def split_window(self, features):
  inputs = features[:, self.input_slice, :]
  labels = features[:, self.labels_slice, :]
  if self.label_columns is not None:
    labels = tf.stack(
        [labels[:, :, self.column_indices[name]] for name in self.label_columns],
        axis=-1)

  # Slicing doesn't preserve static shape information, so set the shapes
  # manually. This way the `tf.data.Datasets` are easier to inspect.
  inputs.set_shape([None, self.input_width, None])
  labels.set_shape([None, self.label_width, None])

  return inputs, labels

WindowGenerator.split_window = split_window

#### Create sequence of arrays of all the dataset
def dataset_stack(train_df, window):
    stack = []
    for i in range(0,len(train_df[0::window])):
        start_array = window*i
        end_array = window*i + window
        if len(train_df[start_array:end_array]) < window:
            continue
        else:
            stack.append(np.array(train_df[start_array:end_array]))
    return stack
#stack = dataset_stack()

def plot(self, model=None, plot_col='ATAvg', max_subplots=5):
    inputs, labels = self.example
    plt.figure(figsize=(10, 10))
    plot_col_index = self.column_indices[plot_col]
    max_n = min(max_subplots, len(inputs))
    
    for n in range(max_n):
        plt.subplot(max_n, 1, n+1)
        plt.ylabel(f'{plot_col} [normed]')
        plt.plot(self.input_indices, inputs[n, :, plot_col_index],
             label='Inputs', marker='.', zorder=-10)

        if self.label_columns:
            label_col_index = self.label_columns_indices.get(plot_col, None)
        else:
            label_col_index = plot_col_index
            
        if label_col_index is None:
            continue
            
        plt.scatter(self.label_indices, labels[n, :, label_col_index],
                edgecolors='k', label='Labels', c='#2ca02c', s=64)
        
        if model is not None:
            predictions = model(inputs)
            if self.label_width == 1:
                plt.scatter(self.label_indices, predictions[0, -1, label_col_index],
                  marker='X', edgecolors='k', label='Predictions',
                  c='#ff7f0e', s=64)
            else:
                plt.scatter(self.label_indices, predictions[n, :, label_col_index],
                  marker='X', edgecolors='k', label='Predictions',
                  c='#ff7f0e', s=64)
        if n == 0:
            plt.legend()
            
        plt.xlabel('Time [steps]')

WindowGenerator.plot = plot

def make_dataset(self, data):
  data = np.array(data, dtype=np.float32)

  ds = tf.keras.preprocessing.timeseries_dataset_from_array(
      data=data,
      targets=None,
      sequence_length=self.total_window_size,
      sequence_stride=1,
      shuffle=True,
      batch_size=batch_size,)

  ds = ds.map(self.split_window)

  return ds

WindowGenerator.make_dataset = make_dataset

@property
def train(self):
  return self.make_dataset(self.train_df)

@property
def val(self):
  return self.make_dataset(self.val_df)

@property
def test(self):
  return self.make_dataset(self.test_df)

@property
def example(self):
  """Get and cache an example batch of `inputs, labels` for plotting."""
  result = getattr(self, '_example', None)
  if result is None:
    # No example batch was found, so get one from the `.train` dataset
    result = next(iter(self.train))
    # And cache it for next time
    self._example = result
  return result

WindowGenerator.train = train
WindowGenerator.val = val
WindowGenerator.test = test
WindowGenerator.example = example

def compile_and_fit(model, window,patience=5):
  early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                    patience=patience,
                                                    mode='min')

  model.compile(loss=tf.losses.MeanSquaredError(),
                optimizer=tf.optimizers.Adam(),
                metrics=[tf.metrics.MeanAbsoluteError()])

  history = model.fit(window.train, epochs=MAX_EPOCHS,
                      validation_data=window.val,
                      callbacks=[early_stopping])

  return history

class Baseline(tf.keras.Model):
  def __init__(self, label_index=None):
    super().__init__()
    self.label_index = label_index

  def call(self, inputs):
    if self.label_index is None:
      return inputs
    result = inputs[:, :, self.label_index]
    return result[:, :, tf.newaxis]

class ResidualWrapper(tf.keras.Model):
  def __init__(self, model):
    super().__init__()
    self.model = model

  def call(self, inputs, *args, **kwargs):
    delta = self.model(inputs, *args, **kwargs)

    # The prediction for each timestep is the input
    # from the previous time step plus the delta
    # calculated by the model.
    return inputs + delta

class MultiStepLastBaseline(tf.keras.Model):
  def call(self, inputs):
    return tf.tile(inputs[:, -1:, :], [1, OUT_STEPS, 1])

class RepeatBaseline(tf.keras.Model):
  def call(self, inputs):
    return inputs

class FeedBack(tf.keras.Model):
  def __init__(self, units, out_steps):
    super().__init__()
    self.out_steps = out_steps
    self.units = units
    self.lstm_cell = tf.keras.layers.LSTMCell(units)
    # Also wrap the LSTMCell in an RNN to simplify the `warmup` method.
    self.lstm_rnn = tf.keras.layers.RNN(self.lstm_cell, return_state=True)
    self.dense = tf.keras.layers.Dense(num_features)
def warmup(self, inputs):
  # inputs.shape => (batch, time, features)
  # x.shape => (batch, lstm_units)
  x, *state = self.lstm_rnn(inputs)

  # predictions.shape => (batch, features)
  prediction = self.dense(x)
  return prediction, state
FeedBack.warmup = warmup

def call(self, inputs, training=None):
  # Use a TensorArray to capture dynamically unrolled outputs.
  predictions = []
  # Initialize the lstm state
  prediction, state = self.warmup(inputs)

  # Insert the first prediction
  predictions.append(prediction)

  # Run the rest of the prediction steps
  for n in range(1, self.out_steps):
    # Use the last prediction as input.
    x = prediction
    # Execute one lstm step.
    x, state = self.lstm_cell(x, states=state,
                              training=training)
    # Convert the lstm output to a prediction.
    prediction = self.dense(x)
    # Add the prediction to the output
    predictions.append(prediction)

  # predictions.shape => (time, batch, features)
  predictions = tf.stack(predictions)
  # predictions.shape => (batch, time, features)
  predictions = tf.transpose(predictions, [1, 0, 2])
  return predictions

FeedBack.call = call

def get_predictions(self, model = None, plot_col = ['ATAvg','RHAvg'], plot=False,scaler_type = 'mean'):
    
    accuracy={}
    for col in range(len(plot_col)):
        plot_col_index = self.column_indices[plot_col[col]]
        all_preds=[]
        all_labels =[]
    
        n_batches = len(tuple(self.test))
        if self.shift==1:
            for i in range(n_batches):
                for inputs, labels in self.test.take(i):  # iterate over batches

                    numpy_labels = labels.numpy() ### get labels
                    numpy_inputs = inputs.numpy() ### get inputs
                    preds = model(numpy_inputs) ### make prediction from trained model
                    numpy_preds = preds.numpy() ### get predictions
                    
                    if scaler_type == 'mean':
                        batch_pred =numpy_preds[:,-1,plot_col_index]*test_std[plot_col_index] + test_mean[plot_col_index]
                        batch_label = numpy_labels[:,-1,plot_col_index]*test_std[plot_col_index] + test_mean[plot_col_index]
                    
                    if scaler_type == 'minmax':
                        scaler = MinMaxScaler()
                        obj = scaler.fit(test_df_raw)
                        batch_pred = obj.inverse_transform(numpy_preds[:,-1,:])[:,plot_col_index]
                        batch_label = obj.inverse_transform(numpy_labels[:,-1,:])[:,plot_col_index]
                        
                    if scaler_type == 'robust':
                        scaler = RobustScaler()
                        obj = scaler.fit(test_df_raw)
                        batch_pred = obj.inverse_transform(numpy_preds[:,-1,:])[:,plot_col_index]
                        batch_label = obj.inverse_transform(numpy_labels[:,-1,:])[:,plot_col_index]
                        
                    if scaler_type =='power':
                        scaler = PowerTransformer()
                        obj = scaler.fit(test_df_raw)
                        batch_pred = obj.inverse_transform(numpy_preds[:,-1,:])[:,plot_col_index]
                        batch_label = obj.inverse_transform(numpy_labels[:,-1,:])[:,plot_col_index]
                    
                    if scaler_type =='stand':
                        scaler = StandardScaler()
                        obj = scaler.fit(test_df_raw)
                        batch_pred = obj.inverse_transform(numpy_preds[:,-1,:])[:,plot_col_index]
                        batch_label = obj.inverse_transform(numpy_labels[:,-1,:])[:,plot_col_index]
                        

                    all_preds.extend(batch_pred)
                    all_labels.extend(batch_label)


            r2=round(r2_score(all_labels, all_preds),3)
            mae = round(mean_absolute_error(all_labels, all_preds),3)

            accuracy[plot_col[col]] = {'r2':r2,
                                       'mae':mae}

            if plot:
                ## One sactter plot per variable
                slope, intercept, r_value, p_value, std_err = stats.linregress(all_labels, all_preds)
                fig, ax = plt.subplots(1, 1, figsize=(5, 5))
                ax.scatter(all_labels, all_preds,edgecolors='k', c='#ff5555', s=32)
                ax.set_xlabel(f'True Values {plot_col[col]} [de-normed]')
                ax.set_ylabel(f'Predicted Values {plot_col[col]} [de-normed]')
                lims = [math.floor(min(all_labels)-min(all_labels)*0.1), math.ceil(max(all_labels)+max(all_labels)*0.1)]
                ax.set_xlim(lims)
                ax.set_ylim(lims)
                line = slope*np.array(all_labels)+intercept
                ax.plot(all_labels, line, 'gray',label = f'r2 = {round(r_value**2,3)}')
                ax.legend(loc = 'lower right')


        else:
            for i in range(n_batches):
                #print(f'i = {i}')
                for inputs, labels in self.test.take(i):  # iterate over batches

                    numpy_labels = labels.numpy() ### get labels
                    numpy_inputs = inputs.numpy() ### get inputs
                    preds = model(numpy_inputs) ### make prediction from trined model
                    numpy_preds = preds.numpy() ### get predictions

                    all_preds_by_time = []
                    all_labels_by_time = []
                    

                    for j in range(numpy_labels.shape[1]): ## number of time steps
                        ### get values for each bacth and time and de-normalize
                        #print(f'j = {j}')
                        if scaler_type == 'mean':
                            batch_pred =numpy_preds[:,j,plot_col_index]*train_std[plot_col_index] + train_mean[plot_col_index]
                            batch_label = numpy_labels[:,j,plot_col_index]*train_std[plot_col_index] + train_mean[plot_col_index]
                            
                        if scaler_type == 'minmax':
                            scaler = MinMaxScaler()
                            obj = scaler.fit(test_df_raw)
                            batch_pred =obj.inverse_transform(numpy_preds[:,j,:])[:,plot_col_index]
                            batch_label = obj.inverse_transform(numpy_labels[:,j,:])[:,plot_col_index]

                        all_preds_by_time.extend(batch_pred)
                        #print(f'all_preds_by_time = {len(all_preds_by_time_0)}')
                        all_labels_by_time.extend(batch_label)


                    all_preds.append(all_preds_by_time)
                    all_labels.append(all_labels_by_time)
                    if len(all_preds) >= i:
                        break

                    ## covert to array (shape= i,time*batch_size)
            multi_preds = np.vstack(all_preds)
            multi_labels = np.vstack(all_labels)

            mae_pred = []
            r2_pred = []
            mse_pred =[]
            rmse_pred = []
            for a in np.arange(0,multi_labels.shape[1],step=batch_size):
                mae = mean_absolute_error(multi_labels[:,a:a+batch_size], multi_preds[:,a:a+batch_size])
                mae_pred.append(mae)
                mse = mean_squared_error(multi_labels[:,a:a+batch_size], multi_preds[:,a:a+batch_size])
                mse_pred.append(mse)
                rmse = math.sqrt(mse)
                rmse_pred.append(rmse)
                r2 = round(r2_score(multi_labels[:,a:a+batch_size], multi_preds[:,a:a+batch_size]),3)
                r2_pred.append(r2)
            df = pd.DataFrame(mae_pred, columns=['mae'])
            df['r2']=r2_pred
            df['mse']=mse_pred
            df['rmse']=rmse_pred
            accuracy[plot_col[col]] = {'r2':r2_pred,
                                       'mae':mae_pred,
                                       'mse': mse_pred,
                                       'rmse':rmse_pred}

            if plot:
                fig, ax = plt.subplots(1, 4, figsize=(20, 5))
                plt.suptitle(f'{model}, window: {self.input_width}_{self.shift}',fontsize = 14)
                ax[0].plot(df.index, df.mae, '-o',c='#ff5555')
                ax[0].set_xlabel(f'prediction times {plot_col[col]}')
                ax[0].set_ylabel(f'MAE {plot_col[col]} [de-normed]')
                ax[3].plot(df.index, df.r2,'-o', c='#0ca4b4')
                ax[3].set_xlabel(f'prediction times {plot_col[col]}')
                ax[3].set_ylabel(f'R2 {plot_col[col]} [de-normed]')
                ax[1].plot(df.index, df.mse,'-o', c='#ff5555')
                ax[1].set_xlabel(f'prediction times {plot_col[col]}')
                ax[1].set_ylabel(f'MSE {plot_col[col]} [de-normed]')
                ax[2].plot(df.index, df.rmse, '-o',c='#ff5555')
                ax[2].set_xlabel(f'prediction times {plot_col[col]}')
                ax[2].set_ylabel(f'RMSE {plot_col[col]} [de-normed]')
            
    return accuracy
                       
WindowGenerator.get_predictions = get_predictions

def single_models(station,path,num_features,input_width, OUT_STEPS):
    ### aggragte results
    val_performance = {}
    performance = {}
    r2 ={}
    
    ## window
    window = WindowGenerator(
    input_width=input_width, label_width=1, shift=OUT_STEPS)
    window.plot()
    plt.savefig(f'{path}/{station}_single_{sample_freq}m_w{input_width}_{OUT_STEPS}_window.png',dpi=100)
    
    ### Baseline
    baseline = Baseline()
    baseline.compile(loss=tf.losses.MeanSquaredError(),
                 metrics=[tf.metrics.MeanAbsoluteError()])
    val_performance[f'Baseline_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = baseline.evaluate(window.val)
    performance[f'Baseline_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = baseline.evaluate(window.test, verbose=0)
    r2[f'Baseline_{sample_freq}m_w{input_width}_{OUT_STEPS}']= window.get_predictions(model=baseline,plot=False)
#     window.plot(baseline)
#     plt.savefig(f'{path}/{station}_Single_Baseline_w{input_width}_{OUT_STEPS}_window.png',dpi=100)
    
    ### Dense
    dense = tf.keras.Sequential([
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dense(units=num_features)
    ])
    history = compile_and_fit(dense, window)
    IPython.display.clear_output()
    val_performance[f'Dense_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = dense.evaluate(window.val)
    performance[f'Dense_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = dense.evaluate(window.test, verbose=0)
#     losses = pd.DataFrame(history.history)
#     losses.plot()
#     plt.savefig(f'{path}/{station}_Single_Dense_{sample_freq}_w{input_width}_{OUT_STEPS}_losses.png',dpi=100)
#     window.plot(dense)
#     plt.savefig(f'{path}/{station}_Single_Dense_w{input_width}_{OUT_STEPS}_window.png',dpi=100)
    r2[f'Dense_{sample_freq}m_w{input_width}_{OUT_STEPS}']= window.get_predictions(model=dense,plot=False)
    
    #RNN
    lstm_model = tf.keras.models.Sequential([
    # Shape [batch, time, features] => [batch, time, lstm_units]
    tf.keras.layers.LSTM(32, return_sequences=True),
    # Shape => [batch, time, features]
    tf.keras.layers.Dense(units=num_features)
    ])
    history = compile_and_fit(lstm_model, window)
    IPython.display.clear_output()
    val_performance[f'LSTM_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = lstm_model.evaluate(window.val)
    performance[f'LSTM_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = lstm_model.evaluate(window.test, verbose=0)
#     losses = pd.DataFrame(history.history)
#     losses.plot()
#     plt.savefig(f'{path}/{station}_Single_LSTM_{sample_freq}_w{input_width}_{OUT_STEPS}_losses.png',dpi=100)
#     window.plot(lstm_model)
#     plt.savefig(f'{path}/{station}_Single_LSTM_w{input_width}_{OUT_STEPS}_window.png',dpi=100)
    r2[f'LSTM_{sample_freq}m_w{input_width}_{OUT_STEPS}']= window.get_predictions(model=lstm_model,plot=False)
    
    ### Autoregressive RNN
    residual_lstm = ResidualWrapper(
    tf.keras.Sequential([
    tf.keras.layers.LSTM(32, return_sequences=True),
    tf.keras.layers.Dense(
        num_features,
        # The predicted deltas should start small
        # So initialize the output layer with zeros
        kernel_initializer=tf.initializers.zeros())
    ]))

    history = compile_and_fit(residual_lstm, window)

    IPython.display.clear_output()
    val_performance[f'Residual_LSTM_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = residual_lstm.evaluate(window.val)
    performance[f'Residual_LSTM_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = residual_lstm.evaluate(window.test, verbose=0)
#     losses = pd.DataFrame(history.history)
#     losses.plot()
#     plt.savefig(f'{path}/{station}_Single_Residual_LSTM_{sample_freq}_w{input_width}_{OUT_STEPS}_losses.png',dpi=100)
#     window.plot(lstm_model)
#     plt.savefig(f'{path}/{station}_Single_Residual_LSTM_w{input_width}_{OUT_STEPS}_window.png',dpi=100)
    r2[f'Residual_LSTM_{sample_freq}m_w{input_width}_{OUT_STEPS}']= window.get_predictions(model=residual_lstm,plot=False)
    

    ### Performance
    fig, ax = plt.subplots()
    x = np.arange(len(performance))
    width = 0.3
    metric_name = 'mean_absolute_error'
    metric_index = baseline.metrics_names.index('mean_absolute_error')
    val_mae = [v[metric_index] for v in val_performance.values()]
    test_mae = [v[metric_index] for v in performance.values()]

    ax.bar(x - 0.17, val_mae, width, label='Validation')
    ax.bar(x + 0.17, test_mae, width, label='Test')
    ax.set_xticks(ticks=x)
           
    ax.set_xticklabels(labels=performance.keys(),rotation = 45, ha="right")
    ax.set_ylabel('MAE (average over all outputs)')
    ax.legend()
    plt.savefig(f'{path}/{station}_single_{sample_freq}m_wm{input_width}_{OUT_STEPS}_performance.png', dpi = 100,bbox_inches='tight')
    
    pd.concat({k: pd.DataFrame(v).T for k, v in r2.items()}, axis=0).to_csv(f'{path}/{station}_single_{sample_freq}m_w{input_width}_{OUT_STEPS}_performance_times.csv')
    per = pd.DataFrame.from_dict(multi_performance, orient='index',columns=['loss_test','mae_test'])
    val= pd.DataFrame.from_dict(multi_val_performance, orient='index',columns=['loss_val','mae_val'])
    pd.merge(per, val, how='inner',left_index=True, right_index =True).to_csv(f'{path}/{station}_single_{sample_freq}m_w{input_width}_{OUT_STEPS}_performance_overall.csv')
    
    return per
def multi_models(station, path, num_features,input_width= 24, OUT_STEPS=12):
    ### aggragte results
    multi_val_performance = {}
    multi_performance = {}
    r2 ={}
    
    ## window
    window = WindowGenerator(
    input_width=input_width, label_width=OUT_STEPS, shift=OUT_STEPS)
    window.plot(plot_col=list(window.column_indices.keys())[0])
    plt.savefig(f'{path}/{station}_multi_{sample_freq}m_w{input_width}_{OUT_STEPS}_window.png',dpi=100)
    
    ### Baseline last
    print('Baseline last')
    last_baseline = MultiStepLastBaseline()
    last_baseline.compile(loss=tf.losses.MeanSquaredError(),
                      metrics=[tf.metrics.MeanAbsoluteError()])
    multi_val_performance[f'BaselineLast_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = last_baseline.evaluate(window.val)
    multi_performance[f'BaselineLast_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = last_baseline.evaluate(window.test, verbose=0)
    r2[f'BaselineLast_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = window.get_predictions(model=last_baseline, plot_col =vars_to_analize)
#     window.plot(last_baseline)
#     plt.savefig(f'{path}/{station}_BaselineLast_{sample_freq}_wm{input_width}_{OUT_STEPS}_window.png',dpi=100)
    
    ### Baseline repeat
    if input_width == OUT_STEPS:
        print(f'Baseline repeat')
        repeat_baseline = RepeatBaseline()
        repeat_baseline.compile(loss=tf.losses.MeanSquaredError(),
                        metrics=[tf.metrics.MeanAbsoluteError()])

        multi_val_performance[f'BaselineRepeat_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = repeat_baseline.evaluate(window.val)
        multi_performance[f'BaselineRepeat_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = repeat_baseline.evaluate(window.test, verbose=0)
        r2[f'BaselineRepeat_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = window.get_predictions(model=repeat_baseline,plot_col =vars_to_analize)
#         window.plot(repeat_baseline)
#         plt.savefig(f'{path}/{station}_BaselineRepeat_{sample_freq}_wm{input_width}_{OUT_STEPS}_window.png',dpi=100)
    else:
        print('Skipping Repeat baseline')
    
    ### Single-Shot
    print(f'Single-shot')
    multi_linear_model = tf.keras.Sequential([
    # Take the last time-step.
    # Shape [batch, time, features] => [batch, 1, features]
    tf.keras.layers.Lambda(lambda x: x[:, -1:, :]),
    # Shape => [batch, 1, out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*num_features,
                          kernel_initializer=tf.initializers.zeros()),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, num_features])
    ])

    history = compile_and_fit(multi_linear_model, window)
    IPython.display.clear_output()
    multi_val_performance[f'MultiLinear_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = multi_linear_model.evaluate(window.val)
    multi_performance[f'MultiLinear_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = multi_linear_model.evaluate(window.test, verbose=0)
    r2[f'MultiLinear_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = window.get_predictions(model=multi_linear_model,plot_col =vars_to_analize)
#     losses = pd.DataFrame(history.history)
#     losses.plot()
#     plt.savefig(f'{path}/{station}_MultiLinear_wm{input_width}_{OUT_STEPS}_losses.png',dpi=100)
#     window.plot(multi_linear_model)
#     plt.savefig(f'{path}/{station}_MultiLinear_{sample_freq}_wm{input_width}_{OUT_STEPS}_window.png',dpi=100)
    
    ### Dense
    print(f'Dense')
    multi_dense_model = tf.keras.Sequential([
    # Take the last time step.
    # Shape [batch, time, features] => [batch, 1, features]
    tf.keras.layers.Lambda(lambda x: x[:, -1:, :]),
    # Shape => [batch, 1, dense_units]
    tf.keras.layers.Dense(512, activation='relu'),
    # Shape => [batch, out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*num_features,
                          kernel_initializer=tf.initializers.zeros()),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, num_features])
    ])

    history = compile_and_fit(multi_dense_model, window)
    IPython.display.clear_output()
    multi_val_performance[f'MultiDense_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = multi_dense_model.evaluate(window.val)
    multi_performance[f'MultiDense_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = multi_dense_model.evaluate(window.test, verbose=0)
    r2[f'MultiDense_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = window.get_predictions(model=multi_dense_model,plot_col =vars_to_analize)
#     losses = pd.DataFrame(history.history)
#     losses.plot()
#     plt.savefig(f'{path}/{station}_MultiDense_wm{input_width}_{OUT_STEPS}_losses.png',dpi=100)
#     window.plot(multi_dense_model)
#     plt.savefig(f'{path}/{station}_MultiDense_{sample_freq}_wm{input_width}_{OUT_STEPS}_window.png',dpi=100)
    
    ### CNN
    print(f'CNN')
    CONV_WIDTH = 3
    multi_conv_model = tf.keras.Sequential([
    # Shape [batch, time, features] => [batch, CONV_WIDTH, features]
    tf.keras.layers.Lambda(lambda x: x[:, -CONV_WIDTH:, :]),
    # Shape => [batch, 1, conv_units]
    tf.keras.layers.Conv1D(256, activation='relu', kernel_size=(CONV_WIDTH)),
    # Shape => [batch, 1,  out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*num_features,
                          kernel_initializer=tf.initializers.zeros()),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, num_features])
    ])

    history = compile_and_fit(multi_conv_model, window)
    IPython.display.clear_output()
    multi_val_performance[f'MultiConv_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = multi_conv_model.evaluate(window.val)
    multi_performance[f'MultiConv_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = multi_conv_model.evaluate(window.test, verbose=0)
    r2[f'MultiConv_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = window.get_predictions(model=multi_conv_model,plot_col =vars_to_analize)
#     losses = pd.DataFrame(history.history)
#     losses.plot()
#     plt.savefig(f'{path}/{station}_MultiConv_wm{input_width}_{OUT_STEPS}_losses.png',dpi=100)
#     window.plot(multi_conv_model)
#     plt.savefig(f'{path}/{station}_MultiConv_{sample_freq}_wm{input_width}_{OUT_STEPS}_window.png',dpi=100)
    
    ### RNN
    print(f'RNN')
    multi_lstm_model = tf.keras.Sequential([
    # Shape [batch, time, features] => [batch, lstm_units]
    # Adding more `lstm_units` just overfits more quickly.
    tf.keras.layers.LSTM(32, return_sequences=False),
    # Shape => [batch, out_steps*features]
    tf.keras.layers.Dense(OUT_STEPS*num_features,
                          kernel_initializer=tf.initializers.zeros()),
    # Shape => [batch, out_steps, features]
    tf.keras.layers.Reshape([OUT_STEPS, num_features])
    ])

    history = compile_and_fit(multi_lstm_model, window)
    IPython.display.clear_output()
    multi_val_performance[f'MultiLSTM_model_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = multi_lstm_model.evaluate(window.val)
    multi_performance[f'MultiLSTM_model_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = multi_lstm_model.evaluate(window.test, verbose=0)
    r2[f'MultiLSTM_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = window.get_predictions(model=multi_lstm_model,plot_col =vars_to_analize)
#     losses = pd.DataFrame(history.history)
#     losses.plot()
#     plt.savefig(f'{path}/{station}_MultiLSTM_wm{input_width}_{OUT_STEPS}_losses.png',dpi=100)
#     window.plot(multi_lstm_model)
#     plt.savefig(f'{path}/{station}_MultiLSTM_{sample_freq}_wm{input_width}_{OUT_STEPS}_window.png',dpi=100)
    
    ### Autoregressive RNN
    print(f'Autoregressive RNN')
    feedback_model = FeedBack(units=32, out_steps=OUT_STEPS)
    prediction, state = feedback_model.warmup(window.example[0])
    history = compile_and_fit(feedback_model, window)
    IPython.display.clear_output()
    multi_val_performance[f'AR_LSTM_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = feedback_model.evaluate(window.val)
    multi_performance[f'AR_LSTM_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = feedback_model.evaluate(window.test, verbose=0)
    r2[f'AR_LSTM_{sample_freq}m_w{input_width}_{OUT_STEPS}'] = window.get_predictions(model=multi_lstm_model,plot_col =vars_to_analize)
#     losses = pd.DataFrame(history.history)
#     losses.plot()
#     plt.savefig(f'{path}/{station}_MultiAR_LSTM_{sample_freq}_wm{input_width}_{OUT_STEPS}_losses.png',dpi=100)
#     window.plot(feedback_model)
#     plt.savefig(f'{path}/{station}_MultiAR_LSTM_wm{input_width}_{OUT_STEPS}_window.png',dpi=100)

    ### Plot Performance
    fig, ax = plt.subplots()
    x = np.arange(len(multi_performance))
    width = 0.3
    metric_name = 'mean_absolute_error'
    metric_index = last_baseline.metrics_names.index('mean_absolute_error')
    val_mae = [v[metric_index] for v in multi_val_performance.values()]
    test_mae = [v[metric_index] for v in multi_performance.values()]

    ax.bar(x - 0.17, val_mae, width, label='Validation')
    ax.bar(x + 0.17, test_mae, width, label='Test')
    ax.set_xticks(ticks=x)
           
    ax.set_xticklabels(labels=multi_performance.keys(),rotation = 45, ha="right")
    ax.set_ylabel('MAE (average over all outputs)')
    ax.legend()
    plt.savefig(f'{path}/{station}_multi_{sample_freq}m_w{input_width}_{OUT_STEPS}_performance.png', dpi = 100,bbox_inches='tight')
    
    pd.concat({k: pd.DataFrame(v).T for k, v in r2.items()}, axis=0).to_csv(f'{path}/{station}_multi_{sample_freq}m_w{input_width}_{OUT_STEPS}_performance_times.csv')
    per = pd.DataFrame.from_dict(multi_performance, orient='index',columns=['loss_test','mae_test'])
    val= pd.DataFrame.from_dict(multi_val_performance, orient='index',columns=['loss_val','mae_val'])
    pd.merge(per, val, how='inner',left_index=True, right_index =True).to_csv(f'{path}/{station}_multi_{sample_freq}m_w{input_width}_{OUT_STEPS}_performance_overall.csv')
    
    return per
def plot_times(file,y0=0.5,y1=1.5, nplots = 14, nrows=5, ncols = 3):
    times = pd.read_csv(file)
    models = times['Unnamed: 0'].unique()
    variables = times['Unnamed: 1'].unique()

    colors = ['#c8ea53','#f56420','#7167ce','#15c534','#e9dc09','#38a9f0','#702dae']
    model_color = dict(zip(models,colors))
    
    fig, axes = plt.subplots(nrows,ncols,figsize= (15,15))
    if nrows*ncols - nplots ==1:
        fig.delaxes(axes[4,2]) 
    if nrows*ncols - nplots ==2:
        fig.delaxes(axes[4,1])
        fig.delaxes(axes[4,2]) 
    
    for a, ax in enumerate(axes.flatten()):
        timet =times[times['Unnamed: 1'] == variables[a]]
        if len(models)==1:
            model_start = 0
        else: model_start = 1
        for model in models[model_start:]:
                val_index =timet.index[timet['Unnamed: 0'] ==model].values[0]
                y = json.loads(timet[timet['Unnamed: 0'] ==model].mae[val_index])
                x = np.arange(1,len(y)+1)
                ax.plot(x,y,'-o',color = model_color[model],label=model.split('_')[0])
                ax.set_title(variables[a])
                ax.set_ylim(y0,y1)
                if a==0:
                    ax.legend()
    return plt.savefig(f'{file.split(".")[0]}.png', dpi = 100,bbox_inches='tight')
