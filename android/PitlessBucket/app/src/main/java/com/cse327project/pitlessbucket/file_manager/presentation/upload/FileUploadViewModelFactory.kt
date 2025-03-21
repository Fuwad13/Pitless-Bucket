package com.cse327project.pitlessbucket.file_manager.presentation.upload

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.cse327project.pitlessbucket.core.data.data_source.ApiService

class FileUploadViewModelFactory(private val apiService: ApiService) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return FileUploadViewModel(apiService) as T
    }
}
